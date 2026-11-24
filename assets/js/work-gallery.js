(() => {
  const picker = document.querySelector('.gallery-picker');
  if (!picker) return;

  const tabs = Array.from(picker.querySelectorAll('[role="tab"]'));
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  if (!tabs.length || panels.some(panel => !panel)) return;

  function select(index) {
    tabs.forEach((tab, position) => {
      const selected = position === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[position].hidden = !selected;
    });
  }

  tabs.forEach((tab, index) => {
    const panel = panels[index];
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', tab.id);
    panel.tabIndex = 0;
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      const last = tabs.length - 1;
      let next;
      switch (event.key) {
        case 'ArrowLeft': next = index === 0 ? last : index - 1; break;
        case 'ArrowRight': next = index === last ? 0 : index + 1; break;
        case 'Home': next = 0; break;
        case 'End': next = last; break;
        default: return;
      }
      event.preventDefault();
      select(next);
      tabs[next].focus();
    });
  });

  function selectLinkedPanel() {
    const target = document.getElementById(location.hash.slice(1));
    const index = panels.findIndex(panel => panel.contains(target));
    if (index < 0 || !panels[index].hidden) return;
    select(index);
    target.scrollIntoView({ block: 'start' });
  }

  select(0);
  picker.hidden = false;
  selectLinkedPanel();
  window.addEventListener('hashchange', selectLinkedPanel);
})();
