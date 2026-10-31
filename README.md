# whatsapp-ai-agent

Atendente virtual para o **WhatsApp Web** com IA. O app abre o WhatsApp no navegador, encontra as conversas com mensagens não lidas, lê o que o cliente escreveu, gera a resposta com uma IA e a digita na conversa, como uma pessoa faria.

Funciona com qualquer API compatível com o padrão da OpenAI (Chat Completions): **OpenRouter**, **OpenAI**, **Groq**, **Ollama** (local), **LM Studio** e outras. Para trocar de provedor, basta mudar o `.env`.

## Como funciona

1. Abre o WhatsApp Web num navegador controlado pelo [nodriver](https://github.com/ultrafunkamsterdam/nodriver). O login (QR code) fica salvo para as próximas execuções.
2. A cada `CHECK_INTERVAL` segundos, procura conversas com o contador de mensagens não lidas.
3. Chega na conversa pelo teclado (TAB e setas) e a abre com Enter.
4. Lê as mensagens e separa as **não respondidas** (as do cliente depois da sua última mensagem).
5. Envia para a IA as instruções de `app/prompts/instructions.md`, o histórico da conversa (opcional) e as mensagens pendentes.
6. Digita a resposta caractere por caractere, aperta Enter e fecha a conversa com Esc.

As teclas são enviadas direto para a aba pelo protocolo do Chrome (CDP), então o app não usa o seu teclado nem o mouse.

## Requisitos

- Python 3.12+
- Um navegador baseado no Chromium: Google Chrome ou Chromium (encontrados automaticamente) ou Edge, Brave e outros (informando o caminho em `BROWSER_PATH`). Firefox e Safari não são suportados.
- Uma chave de API do provedor de IA (ou um servidor local, como o Ollama)

Testado no Windows.

## Instalação

```bash
git clone https://github.com/joaopedroleonel/whatsapp-ai-agent.git
cd whatsapp-ai-agent

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuração

### 1. `.env`

Copie o exemplo e preencha:

```bash
cp .env.example .env
```

Só `AI_BASE_URL` e `AI_MODEL` são obrigatórios. Os demais têm valor padrão.

Exemplos de provedor:

```ini
# OpenRouter
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=google/gemma-4-31b-it:free
AI_API_KEY=sk-or-...
AI_EXTRA_BODY={"reasoning": {"enabled": false}}

# OpenAI
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
AI_API_KEY=sk-...

# Ollama (local)
AI_BASE_URL=http://localhost:11434/v1
AI_MODEL=gemma4:e2b
```

Para usar outro navegador Chromium no lugar do Chrome, informe o executável:

```ini
# Edge
BROWSER_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
# Brave
BROWSER_PATH=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
```

### 2. Instruções da IA

Crie o arquivo `app/prompts/instructions.md` com o prompt de sistema: quem é o atendente, as regras e as informações do seu negócio. A pasta `app/prompts/` fica fora do Git (só o `.gitkeep` é versionado), então o seu prompt não é publicado.

Exemplo de estrutura:

```markdown
# Atendente da Loja X

Você é o assistente de atendimento da Loja X no WhatsApp.

## Regras
- Responda só sobre a Loja X. Para outros assuntos, responda: "Só posso ajudar com assuntos da Loja X."
- Use apenas as informações deste documento. Nunca invente preços ou condições.
- Se não souber, diga: "Vou chamar alguém da equipe para te ajudar com isso."
- Respostas curtas, de 1 a 4 frases, em tom de conversa de WhatsApp.

## Produtos
- Produto A: R$ 10,00 ...

## Horários e contato
...
```

## Uso

```bash
python app/main.py
```

Na primeira execução, leia o QR code com o celular (WhatsApp > Aparelhos conectados). Para sair, feche o navegador ou aperte **Ctrl+C**.

## Variáveis do `.env`

| Variável | Padrão | Descrição |
|---|---|---|
| `AI_BASE_URL` | **obrigatória** | URL da API compatível com OpenAI |
| `AI_MODEL` | **obrigatória** | Modelo a usar |
| `AI_API_KEY` | `none` | Chave da API |
| `AI_EXTRA_BODY` | vazio | Parâmetros extras do provedor, em JSON |
| `AI_TEMPERATURE` | `0.2` | Criatividade das respostas |
| `AI_MAX_TOKENS` | `256` | Tamanho máximo da resposta |
| `AI_TIMEOUT` | `60` | Tempo máximo de espera pela IA (s) |
| `AI_HISTORY` | `true` | Envia as mensagens anteriores da conversa para a IA |
| `SENDER_NAME` | vazio | Nome em negrito antes de cada resposta (`*[Nome]*`) |
| `WHATSAPP_URL` | `https://web.whatsapp.com` | URL do WhatsApp Web |
| `BROWSER_PROFILE_DIR` | `app/browser-profile` | Pasta do perfil do navegador (guarda o login) |
| `BROWSER_PATH` | vazio (procura o Chrome) | Executável de outro navegador Chromium (Edge, Brave...) |
| `LOGIN_TIMEOUT` | `300` | Tempo para ler o QR code (s) |
| `CHECK_INTERVAL` | `5` | Intervalo entre as verificações de mensagens (s) |
| `OPEN_TIMEOUT` | `5` | Tempo máximo para a conversa abrir (s) |
| `SEND_WAIT` | `2` | Espera após enviar, antes de fechar a conversa (s) |
| `MAX_TABS` / `MAX_ARROWS` | `60` / `50` | Limite de TABs e setas para chegar na conversa |
| `KEY_DELAY_MIN` / `KEY_DELAY_MAX` | `0.25` / `0.6` | Pausa entre teclas de navegação (s) |
| `TYPING_DELAY_MIN` / `TYPING_DELAY_MAX` | `0.03` / `0.1` | Pausa entre caracteres digitados (s) |
| `LOG_LEVEL` | `INFO` | Nível dos logs: `DEBUG`, `INFO`, `WARNING` ou `ERROR` |

## Logs

Os logs saem no terminal, uma linha por evento, com campos `chave=valor`:

```
2026-10-30 14:03:12 INFO    main         Atendimento iniciado     chat="Maria Silva" id=7f3a nao_lidas=2
2026-10-30 14:03:14 INFO    navigation   Conversa aberta          chat="Maria Silva" id=7f3a tabs=3 setas=4 ms=1812
2026-10-30 14:03:16 INFO    ai           Resposta gerada          chat="Maria Silva" id=7f3a ms=2140 chars=213 fim=stop tokens_in=812 tokens_out=64
2026-10-30 14:03:21 INFO    main         Atendimento concluído    chat="Maria Silva" id=7f3a pendentes=2 chars_enviados=213 ms=9412
```

- Todas as linhas de um mesmo atendimento têm o mesmo `chat` e `id`, o que facilita filtrar (`findstr id=7f3a` / `grep id=7f3a`).
- `ms` é a duração da etapa. `tokens_in`/`tokens_out` vêm do provedor, quando ele informa. `fim=length` indica resposta cortada pelo `AI_MAX_TOKENS`, e gera um aviso.
- Em `INFO` só aparecem metadados. O texto das mensagens dos clientes e das respostas da IA aparece **só em `DEBUG`**, junto com as execuções de JS e as verificações periódicas. Cuidado ao guardar ou compartilhar logs em `DEBUG`: são dados pessoais (LGPD).
- As cores são desligadas quando a saída não é um terminal ou quando `NO_COLOR` está definido. Para salvar em arquivo: `python app/main.py 2> agent.log`.

## Estrutura

```
app/
├── main.py           # loop principal
├── config.py         # leitura do .env
├── log.py            # formato dos logs e contexto do atendimento
├── browser.py        # abre o WhatsApp Web e executa JS na página
├── chat_list.py      # conversas com mensagens não lidas
├── navigation.py     # abre e fecha conversas pelo teclado
├── conversation.py   # lê as mensagens e separa as não respondidas
├── keyboard.py       # teclas e digitação via CDP
├── ai.py             # monta as mensagens e chama a IA
├── js/               # scripts executados dentro do WhatsApp Web
└── prompts/          # instructions.md (não versionado)
```

## Limitações

- **Só as conversas visíveis na lista** (cerca de 20) são verificadas, porque o WhatsApp Web só desenha as que aparecem na tela.
- **O histórico enviado para a IA** é o que está carregado na conversa aberta. Em conversas longas, as mensagens mais antigas ficam de fora.
- **Pensado para conversas individuais.** Grupos não são tratados de forma especial.
- **Atende uma conversa por vez** e uma por ciclo de verificação.
- **Depende da estrutura da página do WhatsApp Web.** Se o WhatsApp mudar a página, os seletores em `app/js/` podem precisar de ajuste.
