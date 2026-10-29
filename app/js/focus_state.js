const rows = [...document.querySelectorAll('[data-testid^="list-item-"]')];
const indexOf = (row) => Number(row.dataset.testid.replace('list-item-', ''));
const nameOf = (row) => row.querySelector('[data-testid="cell-frame-title"] span[title]')?.title;

const focused = document.activeElement?.closest('[data-testid^="list-item-"]');
const target = rows.find((row) => nameOf(row) === ARGS.name);
const selected = rows.find((row) => row.querySelector('[aria-selected="true"]'));

return JSON.stringify({
  focused: focused ? indexOf(focused) : null,
  target: target ? indexOf(target) : null,
  selectedName: selected ? nameOf(selected) : null,
  chatOpen: !!document.querySelector('[data-testid="conversation-panel-messages"]'),
});
