(() => {
  'use strict';
  const language = document.documentElement.lang === 'en' ? 'en' : 'ko';
  const storageKey = 'tj-portfolio-language';
  let preference = null;
  try { preference = localStorage.getItem(storageKey); } catch (_) { /* Static links remain usable. */ }

  // A return to the unqualified home URL restores the visitor's explicit choice.
  const isHome = !!document.getElementById('home');
  const isEnglishFile = /\.en\.html$/.test(location.pathname);
  if (isHome && !isEnglishFile && preference === 'en') {
    location.replace('index.en.html' + location.search + location.hash);
    return;
  }
  document.querySelectorAll('[data-site-lang]').forEach(link => {
    if (location.hash) link.hash = location.hash;
    link.addEventListener('click', () => {
      try { localStorage.setItem(storageKey, link.dataset.siteLang); } catch (_) {}
    });
  });
  if (isEnglishFile) {
    try { localStorage.setItem(storageKey, 'en'); } catch (_) {}
  }

  // January 2019 is the confirmed start of total professional experience.
  // A Seoul calendar year boundary avoids the visitor's timezone changing the anniversary.
  const currentYear = Number(new Intl.DateTimeFormat('en', { timeZone: 'Asia/Seoul', year: 'numeric' }).format(new Date()));
  document.querySelectorAll('[data-career-years]').forEach(node => {
    node.textContent = Math.max(0, currentYear - 2019) + '+';
  });
  const year = document.getElementById('year');
  if (year) year.textContent = currentYear;

  const legacyCases = {
    '#case-01': 'document-automation', '#case-02': 'construction-progress',
    '#case-03': 'digital-twin', '#case-04': 'drawing-information',
    '#case-05': 'asset-master-data', '#case-06': 'operations-analytics'
  };
  if (isHome && legacyCases[location.hash]) {
    location.replace('projects/' + legacyCases[location.hash] + (language === 'en' ? '.en.html' : '.html'));
    return;
  }
  if (!('IntersectionObserver' in window)) return;
  const navigation = document.querySelector('header nav');
  if (!navigation || !isHome) return;
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
