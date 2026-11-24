const sectionLinks = [...document.querySelectorAll('.nav-shell nav a[href^="#"]:not(.nav-resume)')];
const sections = sectionLinks.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);

function markCurrentSection() {
  const nav = document.querySelector('.nav-shell');
  const threshold = getComputedStyle(nav).position === 'fixed' ? nav.getBoundingClientRect().bottom + 48 : 80;
  let current;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section.id;
  }
  const lastSection = sections[sections.length - 1];
  // A short final section may not reach the threshold before scrolling ends.
  const atPageEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 2;
  if (lastSection && atPageEnd && lastSection.getBoundingClientRect().top < innerHeight) current = lastSection.id;
  if (lastSection && lastSection.getBoundingClientRect().bottom < 0) current = undefined;
  for (const link of sectionLinks) {
    if (link.hash === `#${current}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}

if (sections.length) {
  let scheduled = false;
  addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { markCurrentSection(); scheduled = false; });
  }, { passive: true });
  addEventListener('resize', markCurrentSection);
  addEventListener('hashchange', markCurrentSection);
  addEventListener('pageshow', markCurrentSection);
  markCurrentSection();
}
