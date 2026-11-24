const masthead = document.querySelector('.portfolio-header');
const sectionLinks = [...document.querySelectorAll('.portfolio-header nav a[href^="#"]')];
const sections = [...document.querySelectorAll('main [id]')].filter(section =>
  sectionLinks.some(link => link.hash === `#${section.id}`)
);

function headerOffset() {
  return getComputedStyle(masthead).position === 'sticky' ? masthead.offsetHeight : 0;
}

function markCurrentSection() {
  const threshold = headerOffset() + 48;
  let current;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section.id;
  }
  const lastSection = sections[sections.length - 1];
  // A short final section may not reach the threshold before scrolling ends.
  const atPageEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 2;
  if (lastSection && atPageEnd && lastSection.getBoundingClientRect().top < innerHeight) {
    const target = sections.find(section => `#${section.id}` === location.hash);
    const bounds = target?.getBoundingClientRect();
    current = bounds && bounds.bottom > headerOffset() && bounds.top < innerHeight ? target.id : lastSection.id;
  }
  if (lastSection && lastSection.getBoundingClientRect().bottom < 0) current = undefined;
  for (const link of sectionLinks) {
    if (link.hash === `#${current}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}

if (sections.length) {
  function updateHeader() {
    document.documentElement.style.scrollPaddingTop = `${headerOffset() + 16}px`;
    markCurrentSection();
  }
  let scheduled = false;
  addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { markCurrentSection(); scheduled = false; });
  }, { passive: true });
  addEventListener('resize', updateHeader);
  if ('ResizeObserver' in window) new ResizeObserver(updateHeader).observe(masthead);
  addEventListener('hashchange', markCurrentSection);
  addEventListener('pageshow', markCurrentSection);
  updateHeader();
}
