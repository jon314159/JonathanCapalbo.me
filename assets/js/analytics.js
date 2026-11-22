(() => {
  if (location.protocol !== 'https:' || !['jonathancapalbo.me', 'www.jonathancapalbo.me'].includes(location.hostname)) return;

  const source = location.pathname === '/' || location.pathname === '/index.html'
    ? 'home'
    : location.pathname.replace(/^\//, '').replace(/\.html$/, '');

  const roles = new Map([
    ['business-analyst', 'Business analyst'],
    ['reporting-analyst', 'Reporting analyst'],
    ['systems-operations', 'Systems and service operations'],
    ['project-coordinator', 'Project coordinator'],
  ]);
  const taggedLinks = [];
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
    } else if (target.hostname === 'public.tableau.com') {
      action = 'tableau-public';
      title = 'Tableau Public dashboard';
    } else if (['jonathancapalbo.me', 'www.jonathancapalbo.me'].includes(target.hostname)) {
      if (['/resume.pdf', '/downloads/Jonathan_Capalbo_Business_Analyst_Resume.pdf'].includes(target.pathname)) {
        action = 'resume-default';
        title = 'Business analyst resume link';
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
    taggedLinks.push({ link, action, title, target });
    link.dataset.goatcounterNoSession = '1';
  }

  const incomingRole = new URLSearchParams(location.search).get('role');
  let activeRole = roles.has(incomingRole) ? incomingRole : '';
  let lastPanel = '';
  const pendingViews = [];

  function sendPendingViews() {
    if (!window.goatcounter?.count) return;
    for (const role of pendingViews.splice(0)) {
      window.goatcounter.count({
        path: `view/role/${role}`,
        title: `${roles.get(role)} work samples`,
        event: true,
        no_session: true,
      });
    }
  }

  function updateRole() {
    const hash = location.hash.slice(1);
    const panel = source === 'home' && roles.has(hash) ? hash : '';
    if (panel) activeRole = panel;

    for (const { link, action, title, target } of taggedLinks) {
      const roleSuffix = activeRole ? `/role/${activeRole}` : '';
      link.dataset.goatcounterClick = `click/${action}/from/${source}${roleSuffix}`;
      link.dataset.goatcounterTitle = activeRole
        ? `${title} (from ${source}, ${roles.get(activeRole)})`
        : `${title} (from ${source})`;
      if (activeRole && action.startsWith('project/')) {
        const destination = new URL(target);
        destination.searchParams.set('role', activeRole);
        link.href = destination.href;
      }
    }

    if (document.visibilityState !== 'visible') return;
    if (panel && panel !== lastPanel) pendingViews.push(panel);
    lastPanel = panel;
    sendPendingViews();
  }

  window.goatcounter = {
    path: location.pathname === '/index.html' ? '/' : location.pathname
  };
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://gc.zgo.at/count.js';
  script.setAttribute('data-goatcounter', 'https://jonathancapalbo.goatcounter.com/count');
  script.addEventListener('load', sendPendingViews);
  if (source === 'home') {
    window.addEventListener('hashchange', updateRole);
    document.addEventListener('visibilitychange', updateRole);
  }
  updateRole();
  document.head.appendChild(script);
})();
