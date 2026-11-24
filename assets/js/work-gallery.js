(() => {
  const picker = document.querySelector('.gallery-picker');
  if (!picker) return;

  const tabs = Array.from(picker.querySelectorAll('[role="tab"]'));
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  if (!tabs.length || panels.some(panel => !panel)) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const indicator = document.createElement('span');
  indicator.className = 'gallery-tab-rule';
  indicator.setAttribute('aria-hidden', 'true');
  let selectedIndex = -1;
  let outgoingVisual;
  let animations = [];

  function stopMotion() {
    animations.forEach(animation => animation.cancel());
    animations = [];
    outgoingVisual?.remove();
    outgoingVisual = null;
  }

  function transition(panel, previousVisual, previousRule, direction) {
    const visual = panel.querySelector('.gallery-visual');
    const story = panel.querySelector('.gallery-story');
    const nextRule = indicator.getBoundingClientRect();
    const easing = 'cubic-bezier(.3, 0, .18, 1)';
    const ruleStart = `translate(${previousRule.x - nextRule.x}px, ${previousRule.y - nextRule.y}px) scaleX(${previousRule.width / nextRule.width})`;

    // The outgoing artwork stays on top until the wipe exposes the new selection.
    outgoingVisual = previousVisual.cloneNode(true);
    outgoingVisual.classList.add('gallery-outgoing');
    outgoingVisual.inert = true;
    outgoingVisual.setAttribute('aria-hidden', 'true');
    outgoingVisual.style.height = `${visual.getBoundingClientRect().height}px`;
    visual.after(outgoingVisual);

    const wipe = outgoingVisual.animate([
      { clipPath: 'inset(0 0% 0 0%)' },
      { clipPath: direction > 0 ? 'inset(0 0% 0 100%)' : 'inset(0 100% 0 0%)' },
    ], { duration: 460, easing, fill: 'forwards' });
    animations = [
      wipe,
      story.animate([
        { opacity: 0, transform: `translateX(${direction * 16}px)` },
        { opacity: 1, transform: 'translateX(0)' },
      ], { duration: 400, easing }),
      indicator.animate([{ transform: ruleStart }, { transform: 'none' }], { duration: 360, easing }),
    ];
    const snapshot = outgoingVisual;
    wipe.onfinish = () => {
      if (outgoingVisual === snapshot) stopMotion();
    };
  }

  function select(index, animate = false, direction = Math.sign(index - selectedIndex)) {
    if (index === selectedIndex) return;
    const previousVisual = panels[selectedIndex]?.querySelector('.gallery-visual');
    const previousRule = indicator.getBoundingClientRect();
    stopMotion();
    tabs.forEach((tab, position) => {
      const selected = position === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[position].hidden = !selected;
    });
    tabs[index].append(indicator);
    selectedIndex = index;
    if (animate && previousVisual && previousRule.width && !reducedMotion.matches && indicator.animate) {
      transition(panels[index], previousVisual, previousRule, direction);
    }
  }

  tabs.forEach((tab, index) => {
    const panel = panels[index];
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', tab.id);
    panel.tabIndex = 0;
    tab.addEventListener('click', () => select(index, true));
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
      const direction = event.key === 'ArrowRight' || event.key === 'End' ? 1 : -1;
      select(next, true, direction);
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
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) stopMotion(); });
})();
