const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../script.js'), 'utf8');

function run({date = '2026-10-23T00:00:00Z', language = 'ko', preference = null,
  pathname = '/profile/index.html', hash = '', home = true, blockedStorage = false} = {}) {
  const realDate = Date;
  class Clock extends realDate { constructor(...args) { super(...(args.length ? args : [date])); } }
  const career = {textContent: ''}, year = {textContent: ''}, listeners = {}, writes = [];
  const links = ['ko', 'en'].map(lang => ({dataset: {siteLang: lang}, addEventListener(event, handler) { listeners[lang] = handler; }}));
  let redirected;
  const context = {
    Date: Clock, Intl, window: {},
    localStorage: {
      getItem() { if (blockedStorage) throw Error('blocked'); return preference; },
      setItem(key, value) { if (blockedStorage) throw Error('blocked'); writes.push([key, value]); }
    },
    location: {pathname, hash, search: '', replace(value) { redirected = value; }},
    document: {
      documentElement: {lang: language},
      getElementById(id) { return id === 'home' ? (home ? {} : null) : id === 'year' ? year : null; },
      querySelectorAll(selector) { return selector === '[data-career-years]' ? [career] : selector === '[data-site-lang]' ? links : []; }
    }
  };
  vm.runInNewContext(source, context);
  return {career: career.textContent, year: year.textContent, redirected, writes, listeners};
}

test('experience advances on each January anniversary in Seoul', () => {
  for (const [date, expected] of [
    ['2026-10-23T00:00:00Z','7+'], ['2026-12-31T14:59:59Z','7+'],
    ['2026-12-31T15:00:00Z','8+'], ['2027-12-31T15:00:00Z','9+'],
    ['2018-12-31T14:00:00Z','0+']
  ]) assert.equal(run({date}).career, expected, date);
  assert.equal(run({date:'2026-12-31T15:00:00Z'}).year, 2027);
});
test('an explicitly selected English preference is restored on home', () => {
  assert.equal(run({preference:'en',hash:'#work'}).redirected, 'index.en.html#work');
  assert.equal(run({preference:'ko'}).redirected, undefined);
});
test('language controls store the choice before navigating', () => {
  const result = run(); result.listeners.en(); result.listeners.ko();
  assert.deepEqual(result.writes, [['tj-portfolio-language','en'], ['tj-portfolio-language','ko']]);
});
test('direct English pages remember English; Korean detail URLs remain accessible', () => {
  assert.deepEqual(run({pathname:'/profile/index.en.html',language:'en'}).writes, [['tj-portfolio-language','en']]);
  assert.equal(run({home:false,preference:'en',pathname:'/profile/projects/digital-twin.html'}).redirected, undefined);
});
test('blocked browser storage does not break experience or navigation', () => {
  const result = run({blockedStorage:true}); result.listeners.en();
  assert.equal(result.career,'7+'); assert.equal(result.redirected,undefined);
});
test('legacy project links preserve the current language', () => {
  assert.equal(run({hash:'#case-03'}).redirected, 'projects/digital-twin.html');
  assert.equal(run({hash:'#case-03',language:'en',pathname:'/profile/index.en.html'}).redirected, 'projects/digital-twin.en.html');
});
