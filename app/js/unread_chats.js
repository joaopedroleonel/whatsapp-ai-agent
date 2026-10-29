const clean = (s) => (s || '').replace(/[\u202A\u202C]/g, '').trim();

return JSON.stringify([...document.querySelectorAll('[data-testid^="list-item-"]')].flatMap((row) => {
  const badge = row.querySelector('[data-testid="icon-unread-count"]');
  if (!badge) return [];
  return [{
    index: Number(row.dataset.testid.replace('list-item-', '')),
    name: row.querySelector('[data-testid="cell-frame-title"] span[title]')?.title,
    unread: Number(badge.textContent) || 1,
    time: clean(row.querySelector('[data-testid="chat-list-timestamp"]')?.textContent),
    lastMessage: clean(row.querySelector('[data-testid="last-msg-status"]')?.title),
  }];
}));
