(() => {
  'use strict';
  const panels=[...document.querySelectorAll('[data-v2-panel]')];
  if (!panels.length) return;
  const navigation=[...document.querySelectorAll('[data-v2-nav]')];
  const projectLinks=[...document.querySelectorAll('[data-v2-project]')];
  const languageLinks=[...document.querySelectorAll('[data-site-lang]')];
  const language=document.documentElement.lang==='ko'?'ko':'en';
  const subnav=document.querySelector('.v2-subnav');
  const label=document.querySelector('[data-v2-current]');
  let current='home';
  const activate=(fragment,moveFocus=false)=>{
    let id;
    try { id=decodeURIComponent(fragment.replace(/^#/,'')); } catch (_) { id='home'; }
    // Previously shared walkthrough URLs retain the relevant engineering context.
    if(id==='project-document-automation-validation-workflow')id='project-document-automation-engineering';
    let target=document.getElementById(id);
    let panel=target?.closest('[data-v2-panel]');
    if (id==='main') panel=panels.find(p=>p.dataset.v2Panel===current);
    if (!panel) { panel=panels.find(p=>p.dataset.v2Panel==='home');target=panel; }
    current=panel.dataset.v2Panel;
    panels.forEach(p=>{p.hidden=p!==panel;});
    const project=current.startsWith('project-')?current.slice(8):null;
    const section=project?'work':current;
    navigation.forEach(a=>{
      if(a.dataset.v2Nav===section)a.setAttribute('aria-current','page');
      else a.removeAttribute('aria-current');
    });
    projectLinks.forEach(a=>{
      if(a.dataset.v2Project===project)a.setAttribute('aria-current','page');
      else a.removeAttribute('aria-current');
    });
    if(subnav)subnav.hidden=!project;
    if(label)label.textContent=panel.dataset.v2Label;
    languageLinks.forEach(a=>{a.hash=location.hash;});
    document.title=panel.dataset.v2Label+' — TJ Lee';
    if(moveFocus){
      const heading=panel.querySelector('h2');
      if(heading){heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});}
    }
    requestAnimationFrame(()=>{
      if(target&&target!==panel&&id!=='main')target.scrollIntoView({block:'start',behavior:'instant'});
      else window.scrollTo({top:0,left:0,behavior:'instant'});
    });
  };
  window.addEventListener('hashchange',()=>activate(location.hash,true));
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click',event=>{
      if(a.hash===location.hash){event.preventDefault();activate(a.hash,true);}
    });
  });
  activate(location.hash);
})();
