(() => {
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Preserve external links to the former in-page case studies.
  const legacyCases = {
    '#case-01': 'document-automation',
    '#case-02': 'construction-progress',
    '#case-03': 'digital-twin',
    '#case-04': 'drawing-information',
    '#case-05': 'asset-master-data',
    '#case-06': 'operations-analytics'
  };
  if (document.getElementById('home') && legacyCases[location.hash]) {
    location.replace('projects/' + legacyCases[location.hash] + '.html');
    return;
  }

  // Native links, history, and full HTML content work without JavaScript.
  if (!('IntersectionObserver' in window)) return;
  const navigation = document.querySelector('header nav');
  if (!navigation || !document.getElementById('home')) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navigation.querySelectorAll('a').forEach(link => {
        const active = link.hash === '#' + entry.target.id;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-15% 0px -50% 0px' });
  document.querySelectorAll('#work, #approach, #about').forEach(section => observer.observe(section));
})();
