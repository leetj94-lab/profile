const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.join(__dirname,'../v2-script.js'),'utf8');
function run({hash='',language='en'}={}){
  const make=dataset=>({dataset,attrs:{},listeners:{},hidden:false,
    setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},
    addEventListener(k,v){this.listeners[k]=v;},focus(){this.focused=true;}});
  const keys=['home','work','approach','about','contact','project-document-automation'];
  const panels=keys.map(key=>{
    const panel=make({v2Panel:key,v2Label:key});panel.id=key;
    panel.heading=make({});panel.querySelector=()=>panel.heading;panel.closest=()=>panel;return panel;
  });
  const navigation=keys.slice(0,5).map(key=>{const a=make({v2Nav:key});a.hash='#'+key;return a;});
  const projectLinks=[make({v2Project:'document-automation'})];
  const languageLinks=[make({siteLang:'en'}),make({siteLang:'ko'})];
  const subnav={hidden:true},back=make({}),label={textContent:''},events={},scrolls=[];
  const location={hash};
  const target={closest:()=>panels[5],scrollIntoView(){this.scrolled=true;}};
  const document={title:'',documentElement:{lang:language},
    getElementById(id){return id==='project-document-automation-system-flow'?target:panels.find(p=>p.id===id);},
    querySelector(s){return s==='.v2-subnav'?subnav:s==='[data-back-v1]'?back:s==='[data-v2-current]'?label:null;},
    querySelectorAll(s){return s==='[data-v2-panel]'?panels:s==='[data-v2-nav]'?navigation:s==='[data-v2-project]'?projectLinks:s==='[data-site-lang]'?languageLinks:s==='a[href^="#"]'?navigation:[];}};
  vm.runInNewContext(source,{document,location,requestAnimationFrame:fn=>fn(),window:{addEventListener(k,v){events[k]=v;},scrollTo(value){scrolls.push(value);}}});
  return {panels,navigation,projectLinks,languageLinks,subnav,back,label,document,location,target,scrolls,
    navigate(value){location.hash=value;events.hashchange();},visible(){return panels.filter(p=>!p.hidden).map(p=>p.id);}};
}
test('v2 starts with a single overview panel',()=>{
  const r=run();assert.deepEqual(r.visible(),['home']);assert.equal(r.navigation[0].attrs['aria-current'],'page');
});
test('category navigation updates content, title and keyboard focus',()=>{
  const r=run();r.navigate('#approach');assert.deepEqual(r.visible(),['approach']);
  assert.equal(r.navigation[2].attrs['aria-current'],'page');assert.equal(r.panels[2].heading.focused,true);
  assert.equal(r.document.title,'approach — TJ Lee / v2');
});
test('a shared deep link activates its project and nested anchor',()=>{
  const r=run({hash:'#project-document-automation-system-flow'});assert.deepEqual(r.visible(),['project-document-automation']);
  assert.equal(r.subnav.hidden,false);assert.equal(r.projectLinks[0].attrs['aria-current'],'page');
  assert.equal(r.navigation[1].attrs['aria-current'],'page');assert.equal(r.target.scrolled,true);
  assert.equal(r.back.attrs.href,'projects/document-automation.html');
});
test('Korean retains project context across language and version links',()=>{
  const r=run({hash:'#project-document-automation',language:'ko'});
  assert.equal(r.languageLinks[0].hash,'#project-document-automation');
  assert.equal(r.back.attrs.href,'projects/document-automation.ko.html');
  r.navigate('#about');assert.equal(r.back.attrs.href,'index.ko.html#about');assert.equal(r.subnav.hidden,true);
});
test('unknown or malformed routes safely show the overview',()=>{
  assert.deepEqual(run({hash:'#missing'}).visible(),['home']);assert.deepEqual(run({hash:'#%invalid'}).visible(),['home']);
});
test('reselecting the current navigation item restores the panel top',()=>{
  const r=run({hash:'#work'});let prevented=false;
  r.navigation[1].listeners.click({preventDefault(){prevented=true;}});
  assert.equal(prevented,true);assert.equal(r.scrolls.length,2);assert.equal(r.scrolls[1].top,0);
});
