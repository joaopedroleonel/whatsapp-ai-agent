const messages = [...document.querySelectorAll('[data-pre-plain-text]')].map((el) => {
  const [, time, date, from] = /\[(.+?), (.+?)\] (.*?):/.exec(el.dataset.prePlainText);
  const bubble = el.closest('[data-testid^="conv-msg-"]');
  return {
    date, time, from,
    fromMe: !!bubble.querySelector('[data-testid="msg-meta"] [aria-label], [data-icon="tail-out"]'),
    text: (el.querySelector('[data-testid="selectable-text"]')?.textContent || '').trim(),
  };
});

const me = messages.find((m) => m.fromMe)?.from;
const contact = messages.find((m) => !m.fromMe)?.from;
return JSON.stringify(messages.map((m) => ({ ...m, to: m.fromMe ? contact : me })));
