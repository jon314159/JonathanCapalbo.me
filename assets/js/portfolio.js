const sectionLinks = [...document.querySelectorAll('.nav-shell nav a[href^="#"]')];
const sections = sectionLinks.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);

function markCurrentSection() {
  const nav = document.querySelector('.nav-shell');
  const threshold = getComputedStyle(nav).position === 'fixed' ? nav.getBoundingClientRect().bottom + 48 : 80;
  let current;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section.id;
  }
  if (sections.length && sections[sections.length - 1].getBoundingClientRect().bottom < 0) current = undefined;
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
  markCurrentSection();
}

if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  try {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('project-enter');
        observer.unobserve(entry.target);
      }
    }, { threshold: 0.12 });
    document.querySelectorAll('.featured-project, .project-card').forEach(card => {
      if (card.getBoundingClientRect().top >= innerHeight) observer.observe(card);
    });
  } catch {
    // Cards remain visible if the optional entrance effect is unavailable.
  }
}
