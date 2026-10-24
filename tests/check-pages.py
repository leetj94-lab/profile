#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit
import json, re

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.stack=[];self.errors=[];self.h1=0;self.lang='';self.metrics=[];self.in_metric=False;self.disclosures=0
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='html':self.lang=a['lang']
        if 'id' in a:self.ids.append(a['id'])
        if t=='h1':self.h1+=1
        for k in ['src','href']:
            if a.get(k):self.links.append((t,a[k],a.get('data-site-lang')))
        if a.get('class')=='disclosure':self.disclosures+=1
        if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(t)
    def handle_endtag(self,t):
        if not self.stack or self.stack[-1]!=t:self.errors.append(t)
        else:self.stack.pop()

data=json.loads((ROOT/'content/portfolio.json').read_text())
def bilingual(value):
    if isinstance(value,dict):
        if 'en'in value or 'ko'in value:assert set(value)=={'en','ko'} and all(isinstance(v,str) and v.strip() for v in value.values())
        else:
            for v in value.values():bilingual(v)
    elif isinstance(value,list):
        for v in value:bilingual(v)
bilingual(data)
parsed={}
for filename,lang in [('index.html','en'),('index.en.html','en'),('index.ko.html','ko')]:
    p=ROOT/filename;c=Page();s=p.read_text();c.feed(s);parsed[p]=c
    assert c.lang==lang and c.h1==1 and not c.errors and not c.stack and len(c.ids)==len(set(c.ids)),p
    assert all(key in c.ids for key in ['home','work','approach','about','contact'])
    assert s.count('data-v2-panel=')==11 and 'data-version="2"' in s
    assert 'data-back-v1' not in s and 'version2.html' not in s and 'VERSION 2' not in s
    assert not re.search(r'href="(?:archive/|projects/)',s)
    assert c.disclosures==6
    for record in data['projects']:
        assert 'project-'+record['slug'] in c.ids
        for value,label in record['metrics']:assert value in s
        for token in record['stack']:assert escape(token) in s
assert (ROOT/'index.html').read_bytes()==(ROOT/'index.en.html').read_bytes()
# Keep the approved narrative and role scope consistent across both languages.
expected=['asset-master-data','drawing-information','digital-twin','document-automation','operations-analytics','engineering-agents']
assert [p['slug'] for p in data['projects']]==expected
for name in ['index.html','index.ko.html']:
    html=(ROOT/name).read_text()
    home=html.split('id="home"',1)[1].split('</section>',1)[0]
    about=html.split('id="about"',1)[1].split('</section>',1)[0]
    assert home.count('data-career-years')==1 and 'since 2020' not in home
    assert 'technical lead' not in html.lower() and '기술 리드' not in html
    assert 'U.S. rollout' not in about and '미국 배포' not in about
    assert 'career-growth' in about and 'project-journey' in html
    assert html.count('class="project-rollout"')==1
    assert html.count('class="project-context"')==6
    assert html.count('class="case-section engineering-depth"')==6
    assert html.count('class="implementation-scope"')==6
    assert html.count('class="verification-detail"')==6
    assert html.count('class="mes-operations"')==1
    assert html.count('class="stage-io"')==sum(len(p['flow']) for p in data['projects'])
    for record in data['projects']:
        assert len(record['stage_details'])==len(record['flow'])
        positions=[html.index('id="project-'+record['slug']+'-'+key+'"') for key in ['before-after','results','my-build','system-flow','engineering']]
        assert positions==sorted(positions)
        lang='en' if name=='index.html' else 'ko'
        for stage in record['stage_details']:
            for key in ['input','output','example']:assert escape(stage[key][lang]) in html
    assert 'href="#mes-operations"' in html

    assert not re.search(r'hypothetical|placeholder|lorem ipsum|가상시나리오|가상 시나리오|추측한 정보|사실과 다릅니다',html,re.I)
    for record in data['projects']:
        section=html.split('id="project-'+record['slug']+'"',1)[1]
        for key in ['engineering','system-flow','my-build','results']:
            assert 'id="project-'+record['slug']+'-'+key+'"' in section
        for decision in record['engineering']['decisions']:
            for key in ['title','challenge','choice','reason']:assert escape(decision[key]['en' if name=='index.html' else 'ko']) in section
        for v in record['engineering']['verification']:
            assert escape(v['expected']['en' if name=='index.html' else 'ko']) in section

    master=html.split('id="project-asset-master-data"',1)[1].split('id="project-drawing-information"',1)[0]
    assert 'class="project-rollout"' in master


for p,c in parsed.items():
    for tag,link,switch in c.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(p.parent/u.path).resolve() if u.path else p
        assert target.exists(),(p,link)
        if u.fragment and target in parsed:assert u.fragment in parsed[target].ids,(p,link)
        if tag=='a' and u.path.endswith('.html') and not switch:assert ('.ko.html' in target.name)==(c.lang=='ko'),(p,link)
out=ROOT/'_site'
assert out.exists() and not (out/'archive').exists()
assert not list(out.rglob('README.md')) and not (out/'tools').exists()
for page in [*out.glob('version2*.html'),*out.glob('projects/*.html')]:
    s=page.read_text();assert 'location.replace' in s and 'data-v2-panel' not in s
for page in out.rglob('*.html'):
    assert 'data-back-v1' not in page.read_text()
print('PASS: selected portfolio, 11 panels, metric/stack parity, locale links, HTML/assets, redirects and archive exclusion.')
