(() => {
  if (location.protocol !== 'https:' || !['jonathancapalbo.me', 'www.jonathancapalbo.me'].includes(location.hostname)) return;

  const source = location.pathname === '/' || location.pathname === '/index.html'
    ? 'home'
    : location.pathname.replace(/^\//, '').replace(/\.html$/, '');

  for (const link of document.querySelectorAll('a[href]')) {
    const target = new URL(link.href, location.href);
    let action;
    let title;

    if (target.protocol === 'mailto:') {
      action = 'email';
      title = 'Email link';
    } else if (target.hostname === 'github.com') {
      action = target.pathname.startsWith('/jon314159') ? 'github' : 'github-upstream';
      title = action === 'github' ? 'GitHub link' : 'Upstream GitHub link';
    } else if (['linkedin.com', 'www.linkedin.com'].includes(target.hostname)) {
      action = 'linkedin';
      title = 'LinkedIn link';
    } else if (['jonathancapalbo.me', 'www.jonathancapalbo.me'].includes(target.hostname)) {
      if (target.pathname === '/resume.pdf') {
        action = 'resume-default';
        title = 'Default resume link';
      } else if (target.pathname === '/downloads/Jonathan_Capalbo_Reporting_Operations_Resume.pdf') {
        action = 'resume-reporting-operations';
        title = 'Reporting / operations resume link';
      } else if (link.hasAttribute('download') || target.pathname.startsWith('/downloads/')) {
        action = `download/${target.pathname.split('/').pop()}`;
        title = `Download link: ${target.pathname.split('/').pop()}`;
      } else if (target.pathname.endsWith('.html') && target.pathname !== '/index.html' && target.pathname !== location.pathname) {
        action = `project/${target.pathname.slice(1).replace(/\.html$/, '')}`;
        title = `Project link: ${target.pathname.slice(1).replace(/\.html$/, '')}`;
      }
    }

    if (!action) continue;
    link.setAttribute('data-goatcounter-click', `click/${action}/from/${source}`);
    link.setAttribute('data-goatcounter-title', `${title} (from ${source})`);
    link.setAttribute('data-goatcounter-no-session', '1');
  }

  window.goatcounter = {
    path: location.pathname === '/index.html' ? '/' : location.pathname
  };
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://gc.zgo.at/count.js';
  script.setAttribute('data-goatcounter', 'https://jonathancapalbo.goatcounter.com/count');
  document.head.appendChild(script);
})();
