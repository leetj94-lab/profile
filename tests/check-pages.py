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
stems=['index']+['projects/'+p['slug'] for p in data['projects']]
parsed={}
for stem in stems:
    for suffix,lang in [('.html','en'),('.en.html','en'),('.ko.html','ko')]:
        p=ROOT/(stem+suffix);s=p.read_text();c=Page();c.feed(s);parsed[p]=c
        assert c.lang==lang and c.h1==1 and not c.stack and not c.errors and len(c.ids)==len(set(c.ids)),p
        assert not re.search(r'hypothetical|DRAFT MAPPING|DESIGN EXAMPLE|가상 설계|예상 시나리오|가상 분석',s,re.I),p
        if stem!='index':
            assert c.disclosures==1 and all(i in c.ids for i in ['before-after','system-flow','my-build','results']),p
            assert len(re.findall(r'data-flow-select=',s))==len(re.findall(r'data-flow-panel=',s)),p
        else:assert 'data-career-years' in s and '2019' in s
    # English aliases have identical semantics and markup.
    assert (ROOT/(stem+'.html')).read_bytes()==(ROOT/(stem+'.en.html')).read_bytes()
for p,c in parsed.items():
    for tag,link,switch in c.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(p.parent/u.path).resolve() if u.path else p
        assert target.exists(),(p,link)
        if u.fragment and target in parsed:assert u.fragment in parsed[target].ids,(p,link)
        if tag=='a' and u.path.endswith('.html') and not switch:assert ('.ko.html' in target.name)==(c.lang=='ko'),(p,link)
for p in data['projects']:
    en=(ROOT/'projects'/(p['slug']+'.html')).read_text();ko=(ROOT/'projects'/(p['slug']+'.ko.html')).read_text()
    for value,label in p['metrics']:assert value in en and value in ko
    for token in p['stack']:assert escape(token) in en and escape(token) in ko
print('PASS: 21 pages, six paired project records, metric/stack parity, complete locale links, HTML, assets, sections and disclosure checks.')
