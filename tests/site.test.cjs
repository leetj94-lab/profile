const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../script.js'), 'utf8');

function run({date='2026-10-24T00:00:00Z', language='en', preference=null,
  pathname='/profile/index.html', hash='', home=true, blockedStorage=false, withFlow=false, version=null, mobile=false, reducedMotion=false}={}) {
  const RealDate=Date;
  class Clock extends RealDate { constructor(...args) { super(...(args.length ? args : [date])); } }
  const career={textContent:''}, year={textContent:''}, writes=[], languageListeners={};
  const links=['en','ko'].map(lang=>({dataset:{siteLang:lang},addEventListener(event,fn){languageListeners[lang]=fn;}}));
  const buttons=Array.from({length:3},(_,i)=>({attrs:{'aria-pressed':String(i===0)},listeners:{},focused:false,
    addEventListener(event,fn){this.listeners[event]=fn;},setAttribute(k,v){this.attrs[k]=v;},focus(){this.focused=true;}}));
  const panels=buttons.map((_,i)=>({hidden:i!==0,scrollIntoView(value){this.scrollOptions=value;}}));
  const flow={querySelectorAll(selector){return selector==='[data-flow-select]'?buttons:panels;}};
  let redirected;
  vm.runInNewContext(source,{
    Date:Clock,Intl,window:{matchMedia(query){return {matches:query.includes("prefers-reduced-motion")?reducedMotion:mobile};}},
    localStorage:{getItem(){if(blockedStorage)throw Error('blocked');return preference;},setItem(k,v){if(blockedStorage)throw Error('blocked');writes.push([k,v]);}},
    location:{pathname,hash,search:'',replace(value){redirected=value;}},
    document:{body:{dataset:{version}},documentElement:{lang:language},getElementById(id){return id==='home'?(home?{}:null):id==='year'?year:null;},
      querySelectorAll(s){return s==='[data-career-years]'?[career]:s==='[data-site-lang]'?links:s==='[data-flow]'&&withFlow?[flow]:[];}}
  });
  return {career:career.textContent,year:year.textContent,redirected,writes,languageListeners,links,buttons,panels};
}
test('English is the default without a saved preference',()=>{
  const r=run();assert.equal(r.redirected,undefined);assert.equal(r.career,'7+');assert.deepEqual(r.writes,[]);
});
test('experience advances at Seoul January boundaries',()=>{
  for(const [date,expected] of [['2026-12-31T14:59:59Z','7+'],['2026-12-31T15:00:00Z','8+'],['2027-12-31T15:00:00Z','9+'],['2018-12-31T14:00:00Z','0+']])assert.equal(run({date}).career,expected,date);
  assert.equal(run({date:'2026-12-31T15:00:00Z'}).year,2027);
});
test('home restores explicit Korean preference and preserves the anchor',()=>{
  assert.equal(run({preference:'ko',hash:'#work'}).redirected,'index.ko.html#work');
  assert.equal(run({preference:'en'}).redirected,undefined);
});
test('explicit English and Korean URLs preserve their selected language',()=>{
  assert.equal(run({preference:'ko',pathname:'/profile/index.en.html'}).redirected,undefined);
  assert.deepEqual(run({language:'ko',pathname:'/profile/index.ko.html'}).writes,[['tj-portfolio-language','ko']]);
});
test('language links remember the selection and preserve section context',()=>{
  const r=run({hash:'#about'});r.languageListeners.ko();r.languageListeners.en();
  assert.deepEqual(r.writes,[['tj-portfolio-language','ko'],['tj-portfolio-language','en']]);assert.equal(r.links[1].hash,'#about');
});
test('blocked storage does not break calculation, switches or flow controls',()=>{
  const r=run({blockedStorage:true,withFlow:true});r.languageListeners.ko();r.buttons[2].listeners.click();
  assert.equal(r.career,'7+');assert.equal(r.panels[2].hidden,false);
});
test('legacy case anchors resolve to the current language and project',()=>{
  assert.equal(run({hash:'#case-03'}).redirected,'index.html#project-digital-twin');
  assert.equal(run({language:'ko',pathname:'/profile/index.ko.html',hash:'#case-03'}).redirected,'index.ko.html#project-digital-twin');
  assert.equal(run({hash:'#case-02'}).redirected,'index.html#project-engineering-agents');
});
test('workflow selection exposes only the matching panel and pressed control',()=>{
  const r=run({home:false,withFlow:true});r.buttons[2].listeners.click();
  assert.deepEqual(r.panels.map(p=>p.hidden),[true,true,false]);assert.deepEqual(r.buttons.map(b=>b.attrs['aria-pressed']),['false','false','true']);
});
test('workflow keyboard navigation wraps and supports Home and End',()=>{
  const r=run({home:false,withFlow:true});let prevented=0;
  r.buttons[2].listeners.keydown({key:'ArrowRight',preventDefault(){prevented++;}});
  assert.equal(r.panels[0].hidden,false);assert.equal(r.buttons[0].focused,true);
  r.buttons[0].listeners.keydown({key:'End',preventDefault(){prevented++;}});assert.equal(r.panels[2].hidden,false);
  r.buttons[2].listeners.keydown({key:'Home',preventDefault(){prevented++;}});assert.equal(r.panels[0].hidden,false);assert.equal(prevented,3);
});

test('v2 restores Korean without redirecting to the original site',()=>{
  assert.equal(run({preference:'ko',pathname:'/profile/version2.html',hash:'#approach',version:'2'}).redirected,'index.ko.html#approach');
});

test('mobile stage selection reveals its implementation panel',()=>{
  const r=run({withFlow:true,mobile:true});r.buttons[2].listeners.click();
  assert.equal(r.panels[2].hidden,false);assert.equal(r.panels[2].scrollOptions.block,'start');
  assert.equal(r.panels[2].scrollOptions.behavior,'smooth');
});
test('stage scrolling respects reduced-motion preferences',()=>{
  const r=run({withFlow:true,mobile:true,reducedMotion:true});r.buttons[1].listeners.click();
  assert.equal(r.panels[1].scrollOptions.behavior,'instant');
});
