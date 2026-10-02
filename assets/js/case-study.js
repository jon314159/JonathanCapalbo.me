(() => {
  const main = document.getElementById('case-content');
  if (!main) return;

  const sections = [...main.querySelectorAll('[data-read-label]')];
  if (sections.length > 1) {
    const contents = document.createElement('details');
    contents.className = 'case-contents';
    const summary = document.createElement('summary');
    summary.append('On this page');
    const position = document.createElement('span');
    position.className = 'case-position';
    summary.append(position);
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Sections in this case study');
    const links = sections.map(section => {
      const link = document.createElement('a');
      link.href = `#${section.id}`;
      link.textContent = section.dataset.readLabel;
      nav.append(link);
      return link;
    });
    const progress = document.createElement('div');
    progress.className = 'case-reading-progress';
    progress.setAttribute('aria-hidden', 'true');
    const fill = document.createElement('span');
    progress.append(fill);
    summary.append(progress);
    contents.append(summary, nav);
    main.prepend(contents);

    function updatePosition() {
      const header = document.querySelector('.nav-shell');
      const headerBottom = header && getComputedStyle(header).position === 'fixed'
        ? header.getBoundingClientRect().bottom + 12 : 0;
      contents.style.top = `${headerBottom}px`;
      const offset = headerBottom + summary.getBoundingClientRect().height + 20;
      document.documentElement.style.scrollPaddingTop = `${offset}px`;
      let active = -1;
      sections.forEach((section, index) => {
        if (section.getBoundingClientRect().top <= offset + 24) active = index;
      });
      links.forEach((link, index) => {
        if (index === active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      position.textContent = active < 0 ? 'Choose a section' : sections[active].dataset.readLabel;
      const start = main.offsetTop;
      const distance = Math.max(1, main.offsetHeight - innerHeight);
      fill.style.transform = `scaleX(${Math.max(0, Math.min(1, (scrollY - start) / distance))})`;
    }
    let scheduled = false;
    function scheduleUpdate() {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(() => { updatePosition(); scheduled = false; });
    }
    addEventListener('scroll', scheduleUpdate, { passive: true });
    addEventListener('resize', scheduleUpdate);
    if ('ResizeObserver' in window) new ResizeObserver(scheduleUpdate).observe(main);
    links.forEach((link, index) => link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      contents.open = false;
      updatePosition();
      if (location.hash !== link.hash) history.pushState(null, '', link.hash);
      sections[index].scrollIntoView({ block: 'start', behavior: 'instant' });
      const heading = sections[index].querySelector('h2');
      if (heading) {
        // Move keyboard focus out of the menu before its links become hidden.
        heading.setAttribute('tabindex', '-1');
        heading.focus({ preventScroll: true });
        heading.addEventListener('blur', () => heading.removeAttribute('tabindex'), { once: true });
      }
      updatePosition();
    }));
    contents.addEventListener('keydown', event => {
      if (event.key !== 'Escape') return;
      contents.open = false;
      summary.focus();
    });
    updatePosition();
  }

  const walkthrough = document.getElementById('walkthrough');
  const panels = walkthrough ? [...walkthrough.querySelectorAll('.walkthrough-step')] : [];
  if (panels.length > 1) {
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const controls = document.createElement('div');
    controls.className = 'walkthrough-controls';
    const choices = document.createElement('div');
    choices.className = 'walkthrough-choices';
    choices.setAttribute('role', 'group');
    choices.setAttribute('aria-label', 'Workbook walkthrough steps');
    const labels = ['Daily entry', 'Monthly rollup', 'Dashboard'];
    let index = 0;
    let timer;
    let playing = false;
    const buttons = panels.map((panel, step) => {
      panel.id = `workbook-step-${step + 1}`;
      const image = panel.querySelector('img');
      if (image) {
        const imageStatus = document.createElement('p');
        imageStatus.className = 'walkthrough-image-status';
        imageStatus.setAttribute('role', 'status');
        function updateImageStatus() {
          imageStatus.textContent = !image.complete ? 'Loading workbook screenshot…'
            : image.naturalWidth ? '' : 'Screenshot could not load. Use the full-size image link to try again.';
          imageStatus.hidden = !imageStatus.textContent;
        }
        image.before(imageStatus);
        image.addEventListener('load', updateImageStatus);
        image.addEventListener('error', updateImageStatus);
        updateImageStatus();
      }
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = `${step + 1}. ${labels[step]}`;
      button.setAttribute('aria-controls', panel.id);
      button.addEventListener('click', () => { pause(); show(step); });
      choices.append(button);
      return button;
    });
    const transport = document.createElement('div');
    transport.className = 'walkthrough-transport';
    function makeButton(label, action) {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.addEventListener('click', action);
      transport.append(button);
      return button;
    }
    const previous = makeButton('Previous step', () => { pause(); show(index - 1); });
    const play = makeButton('Play walkthrough', () => {
      if (playing) { pause(); return; }
      if (index === panels.length - 1) show(0);
      playing = true;
      play.textContent = 'Pause walkthrough';
      timer = setInterval(() => {
        show(index + 1);
        if (index === panels.length - 1) pause();
      }, 12000);
    });
    const next = makeButton('Next step', () => { pause(); show(index + 1); });
    const status = document.createElement('p');
    status.className = 'walkthrough-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-atomic', 'true');
    function pause() {
      clearInterval(timer);
      playing = false;
      play.textContent = index === panels.length - 1 ? 'Replay walkthrough' : 'Play walkthrough';
    }
    function show(step) {
      index = Math.max(0, Math.min(panels.length - 1, step));
      panels.forEach((panel, stepIndex) => { panel.hidden = stepIndex !== index; });
      buttons.forEach((button, stepIndex) => button.setAttribute('aria-pressed', String(stepIndex === index)));
      previous.disabled = index === 0;
      next.disabled = index === panels.length - 1;
      status.textContent = `Step ${index + 1} of ${panels.length}: ${labels[index]}.`;
      if (!playing) pause();
    }
    function applyMotionPreference() {
      pause();
      play.hidden = reducedMotion.matches;
    }
    reducedMotion.addEventListener('change', applyMotionPreference);
    document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
    panels.forEach(panel => panel.addEventListener('focusin', pause));
    controls.append(choices, transport, status);
    walkthrough.querySelector('.section-heading').after(controls);
    walkthrough.classList.add('walkthrough-enhanced');
    show(0);
    applyMotionPreference();
  }

  document.querySelectorAll('.sql-query').forEach(pre => {
    const code = pre.querySelector('code');
    if (!code || !code.textContent.trim()) return;
    const source = code.textContent;
    const tokens = /(--[^\n]*|'(?:''|[^'])*'|\b(?:CREATE|OR|REPLACE|VIEW|AS|SELECT|FROM|JOIN|ON|WHERE|IS|NULL|WITH|READ|ONLY|ALTER|SESSION|SET|TABLE|ADD|CONSTRAINT|CHECK|UNIQUE|INDEX|CASE|WHEN|THEN|ELSE|END)\b|\b\d+(?:\.\d+)?\b)/gi;
    const fragment = document.createDocumentFragment();
    let cursor = 0;
    for (const match of source.matchAll(tokens)) {
      fragment.append(source.slice(cursor, match.index));
      const span = document.createElement('span');
      span.className = match[0].startsWith('--') ? 'sql-comment'
        : match[0].startsWith("'") ? 'sql-string'
          : /^\d/.test(match[0]) ? 'sql-number' : 'sql-keyword';
      span.textContent = match[0];
      fragment.append(span);
      cursor = match.index + match[0].length;
    }
    fragment.append(source.slice(cursor));
    code.replaceChildren(fragment);
    const wrapper = document.createElement('div');
    wrapper.className = 'sql-code-block';
    const toolbar = document.createElement('div');
    toolbar.className = 'sql-code-toolbar';
    const label = document.createElement('span');
    const codeLabel = pre.dataset.codeLabel || 'SQL example';
    label.textContent = `${pre.dataset.codeLanguage || 'Oracle SQL'} · ${codeLabel}`;
    const copy = document.createElement('button');
    copy.type = 'button';
    copy.textContent = 'Copy code';
    copy.setAttribute('aria-label', `Copy ${codeLabel.toLowerCase()}`);
    const status = document.createElement('p');
    status.className = 'sql-copy-status';
    status.setAttribute('role', 'status');
    copy.addEventListener('click', async () => {
      copy.disabled = true;
      status.textContent = 'Copying code…';
      try {
        await navigator.clipboard.writeText(source);
        status.textContent = 'Code copied.';
      } catch {
        const selection = getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = 'Clipboard access is unavailable. Code selected; use your browser’s Copy command.';
      } finally {
        copy.disabled = false;
      }
    });
    pre.setAttribute('tabindex', '0');
    pre.setAttribute('aria-label', label.textContent);
    toolbar.append(label, copy);
    pre.before(wrapper);
    wrapper.append(toolbar, pre, status);
  });
})();
