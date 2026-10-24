(() => {
  'use strict';
  const language = document.documentElement.lang === 'ko' ? 'ko' : 'en';
  const storageKey = 'tj-portfolio-language';
  let preference = null;
  try { preference = localStorage.getItem(storageKey); } catch (_) {}
  const isHome = !!document.getElementById('home');
  const homeStem = 'index';
  const explicitEnglish = /\.en\.html$/.test(location.pathname);
  if (isHome && language === 'en' && !explicitEnglish && preference === 'ko') {
    location.replace(homeStem + '.ko.html' + location.search + location.hash);
    return;
  }
  if (language === 'ko' || explicitEnglish) {
    try { localStorage.setItem(storageKey, language); } catch (_) {}
  }
  document.querySelectorAll('[data-site-lang]').forEach(link => {
    if (location.hash) link.hash = location.hash;
    link.addEventListener('click', () => {
      try { localStorage.setItem(storageKey, link.dataset.siteLang); } catch (_) {}
    });
  });
  const currentYear = Number(new Intl.DateTimeFormat('en', { timeZone: 'Asia/Seoul', year: 'numeric' }).format(new Date()));
  document.querySelectorAll('[data-career-years]').forEach(node => {
    node.textContent = Math.max(0, currentYear - 2019) + '+';
  });
  const year = document.getElementById('year');
  if (year) year.textContent = currentYear;
  const legacyCases = {
    '#case-01': 'document-automation', '#case-02': 'engineering-agents',
    '#case-03': 'digital-twin', '#case-04': 'drawing-information',
    '#case-05': 'asset-master-data', '#case-06': 'operations-analytics'
  };
  if (isHome && legacyCases[location.hash]) {
    location.replace(homeStem + (language === 'ko' ? '.ko.html' : '.html') + '#project-' + legacyCases[location.hash]);
    return;
  }
  document.querySelectorAll('[data-flow]').forEach(flow => {
    const buttons = [...flow.querySelectorAll('[data-flow-select]')];
    const panels = [...flow.querySelectorAll('[data-flow-panel]')];
    const select = index => {
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
      panels.forEach((panel, i) => { panel.hidden = i !== index; });
    };
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => select(index));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % buttons.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + buttons.length - 1) % buttons.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = buttons.length - 1;
        else return;
        event.preventDefault(); select(next); buttons[next].focus();
      });
    });
  });
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
