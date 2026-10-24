#!/usr/bin/env python3
"""Render equivalent English/Korean pages from one bilingual content model."""
from pathlib import Path
from html import escape as E
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib
from presentation import ai_section, render_v2

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/portfolio.json').read_text())
PROJECTS=DATA['projects']
YEAR=datetime.now(ZoneInfo('Asia/Seoul')).year
ASSETS={}
for name in ['styles.css','script.js','v2-styles.css','v2-script.js']:
    p=ROOT/name; b=p.read_bytes(); hashed=p.stem+'-'+hashlib.sha256(b).hexdigest()[:10]+p.suffix
    (ROOT/hashed).write_bytes(b);ASSETS[p.stem]=hashed

def text(v,lang): return E(v[lang] if isinstance(v,dict) else str(v))
def S(en,ko,lang): return E(en if lang=='en' else ko)
def route(slug,lang): return slug+('.ko.html' if lang=='ko' else '.html')
def icon(name):
    paths={
    'file':'<path d="M7 3h7l4 4v14H6V3zM14 3v5h5M9 12h6M9 16h6"/>',
    'drawing':'<path d="M4 4h16v16H4zM7 8h10M8 7v10M7 16h10M16 7v10M11 11h2v2h-2z"/>',
    'database':'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 4 16 4 16 0V5M4 12v7c0 4 16 4 16 0v-7"/>',
    'cube':'<path d="m12 2 9 5v10l-9 5-9-5V7zM3 7l9 5 9-5M12 12v10M7 5l10 6"/>',
    'screen':'<rect x="3" y="3" width="18" height="14" rx="2"/><path d="M8 21h8M12 17v4M6 7h12M6 10h5"/>',
    'api':'<path d="m7 6-6 6 6 6M17 6l6 6-6 6M14 3l-4 18"/>',
    'cloud':'<path d="M6 18a5 5 0 0 1-1-10 7 7 0 0 1 13-1 5.5 5.5 0 0 1 0 11M12 12v10m-3-3 3 3 3-3"/>',
    'deploy':'<path d="M4 4h16v6H4zM4 14h16v6H4zM7 7h1M7 17h1M15 10v4M18 10v4"/>',
    'queue':'<path d="M3 5h12M3 12h12M3 19h12m3-13 4 6-4 6M6 5v14"/>',
    'shield':'<path d="m12 2 9 4v6c0 6-9 10-9 10S3 18 3 12V6zM7 12l3 3 7-7"/>',
    'users':'<circle cx="9" cy="7" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6M21 21v-3a6 6 0 0 0-4-6"/>',
    'pulse':'<path d="M2 12h5l3-8 4 16 3-8h5"/>',
    'spark':'<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3zM20 2v4M18 4h4"/>',
    'search':'<circle cx="10" cy="10" r="7"/><path d="m15 15 7 7"/>',
    'code':'<path d="m8 5-7 7 7 7m8-14 7 7-7 7M14 2l-4 20"/>',
    'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>',
    'check':'<path d="m4 12 5 5L20 6"/>',
    }
    return '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths.get(name,paths['code'])+'</svg>'

def head(title,description,lang,prefix,stem):
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#142a43"><meta name="description" content="{description}"><title>{title} — TJ Lee</title><link rel="stylesheet" href="{prefix}{ASSETS['styles']}"><link rel="alternate" hreflang="en" href="{stem}.html"><link rel="alternate" hreflang="ko" href="{stem}.ko.html"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23142a43'/%3E%3Ctext x='12' y='44' font-size='36' font-family='Arial' fill='white'%3Etj%3C/text%3E%3C/svg%3E"></head><body><a class="skip" href="#main">{S('Skip to content','본문으로 이동',lang)}</a>'''

def header(lang,prefix,stem,project=False):
    home=prefix+route('index',lang)
    return f'''<header class="site-header"><a class="wordmark" href="{home}#home" aria-label="{S('TJ Lee home','TJ Lee 홈',lang)}"><span class="monogram">tj.</span><span>TJ LEE<small>SYSTEMS & AUTOMATION</small></span></a><nav aria-label="{S('Main navigation','주 메뉴',lang)}"><a href="{home}#work" {'aria-current="page"' if project else ''}>{S('Selected work','프로젝트',lang)}</a><a href="{home}#approach">{S('AI & approach','AI 활용',lang)}</a><a href="{home}#about">{S('About','소개',lang)}</a></nav><div class="language-switch" role="group" aria-label="{S('Language selection','언어 선택',lang)}"><a href="{stem}.html" data-site-lang="en" lang="en" hreflang="en" {'aria-current="true"' if lang=='en' else ''}>EN</a><a href="{stem}.ko.html" data-site-lang="ko" lang="ko" hreflang="ko" {'aria-current="true"' if lang=='ko' else ''}>한국어</a></div><a class="nav-contact" href="mailto:leetj94@gmail.com">{S('Let’s connect','연락하기',lang)} ↗</a></header>'''

def footer(lang,prefix=''):
    return f'''<footer class="wrap site-footer"><span>© <span id="year">{YEAR}</span> Taekjun (TJ) Lee</span><span>{S('AI-assisted design & development','AI를 활용한 디자인·개발',lang)}</span><a href="https://www.linkedin.com/in/taek-jun-lee-a83160344" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a></footer><script src="{prefix}{ASSETS['script']}"></script></body></html>'''

def disclosure(lang):
    return '<aside class="disclosure">'+icon('shield')+'<p>'+S('Under Korea’s industrial technology protection law and company security policy, implementation details are withheld. This portfolio explains the overall project approach.','산업기술보호법 및 회사 보안정책에 따라 세부 구현은 공개하지 않으며, 프로젝트의 전체적인 컨셉과 접근 방식만 설명합니다.',lang)+'</p></aside>'

def art(p,lang,prefix='',cover=False):
    if not p['image']:
        return '<div class="agent-art" role="img" aria-label="'+text(p['alt'],lang)+'"><div class="agent-question">'+icon('search')+S('Engineering question','엔지니어링 질문',lang)+'</div><div class="agent-path"><span>'+icon('database')+'SQL</span><span>'+icon('api')+'API</span><span>'+icon('file')+S('Cases','사례',lang)+'</span></div><div class="agent-answer">'+icon('spark')+S('Retrieve. Explain. Review.','조회 · 설명 · 검토',lang)+'</div></div>'
    return f'<img src="{prefix}assets/{p["image"]}" width="1536" height="1024" loading="lazy" alt="{text(p["alt"],lang)}">'

def tags(p,limit=None):return '<div class="tags">'+''.join('<span>'+E(s)+'</span>' for s in p['stack'][:limit])+'</div>'

def card(p,lang,flagship=False):
    href='projects/'+route(p['slug'],lang)
    image=art(p,lang)
    image_note=('<span class="image-credit">'+S('AI-generated illustration','AI 생성 이미지',lang)+'</span>') if p['image'] else ''
    return f'''<article class="project-card {'flagship' if flagship else ''}"><a class="project-cover" href="{href}" aria-label="{text(p['title'],lang)}">{image}{image_note}<span class="circle-arrow">↗</span></a><div class="project-copy"><div class="project-meta"><span>{p['number']} / {text(p['category'],lang)}</span><span>{p['period']}</span></div><h3><a href="{href}">{text(p['title'],lang)}</a></h3><p>{text(p['summary'],lang)}</p><div class="card-result"><strong>{E(p['metrics'][0][0])}</strong><span>{text(p['metrics'][0][1],lang)}</span></div>{tags(p,4)}<a class="project-link" href="{href}">{S('Explore the project','상세 보기',lang)} <span>↗</span></a></div></article>'''

def home(lang):
    title=S('From field experience to production systems','현업 경험에서 운영되는 시스템까지',lang)
    desc=S('Taekjun (TJ) Lee — Business Systems and Automation Engineer. Primary developer across requirements, full-stack applications, AWS delivery and production support.','TJ Lee — 현업 요구부터 풀스택 개발, AWS 배포와 운영까지 담당하는 업무 시스템·자동화 엔지니어.',lang)
    s=head(title,desc,lang,'','index')+header(lang,'','index')
    s+=f'''<main id="main"><section id="home" class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span>{S('BUSINESS SYSTEMS & AUTOMATION ENGINEER','업무 시스템 · 자동화 엔지니어',lang)}</p><h1>{S('From the factory floor.','현장을 이해하고',lang)}<br><em>{S('To production systems.','운영되는 시스템으로.',lang)}</em></h1><p class="hero-lead">{S('I’ve been the engineering user. Now I turn those workflows into software—and own the delivery.','시스템을 직접 사용하던 현업 엔지니어에서, 업무를 소프트웨어로 구현하고 운영까지 책임지는 개발자가 됐습니다.',lang)}</p><p class="hero-description">{S('Samsung Electronics · Primary developer across requirements, architecture, backend/frontend, AWS deployment and production support.','삼성전자 · 요구사항·아키텍처·백엔드·프론트엔드·AWS 배포·운영을 담당하는 주 개발자.',lang)}</p><div class="actions"><a class="button dark" href="#work">{S('Explore my work','프로젝트 살펴보기',lang)} ↘</a><a class="text-link" href="#about">{S('Meet TJ','소개 보기',lang)} ↗</a></div><a class="version-link" href="{route('version2',lang)}">{S('Try the streamlined v2','간결한 v2 살펴보기',lang)} ↗</a><p class="relocation">{S('Seoul, Korea · Open to relocation to New Zealand & Australia','서울, 대한민국 · 뉴질랜드·호주 이주 가능',lang)}</p></div><figure class="hero-art"><img src="assets/connected-systems.webp" width="1536" height="1024" fetchpriority="high" alt="{S('Engineering documents, a facility and data connected into a system','엔지니어링 문서·설비·데이터를 시스템으로 연결한 이미지',lang)}"><figcaption>{S('AI-generated concept illustration for understanding the work.','업무 이해를 돕기 위해 AI로 생성한 컨셉 이미지입니다.',lang)}</figcaption></figure></section><section class="credibility wrap" aria-label="{S('Experience summary','경력 요약',lang)}"><div><span class="mini-label">{S('PROFESSIONAL EXPERIENCE','전체 직무 경력',lang)}</span><strong><span data-career-years>{YEAR-2019}+</span> {S('years','년',lang)}</strong><small>{S('Since January 2019','2019년 1월부터',lang)}</small></div><div><span class="mini-label">{S('CURRENT ROLE','현재 역할',lang)}</span><strong>{S('Systems Engineer','시스템 엔지니어',lang)}</strong><small>Samsung Electronics · 2020–{S('present','현재',lang)}</small></div><div><span class="mini-label">{S('OWNERSHIP','책임 범위',lang)}</span><strong>{S('Requirements → build → operate','요구사항 → 개발 → 운영',lang)}</strong><small>{S('Developer · End-to-end project ownership','개발자 · 프로젝트 전 과정 전담',lang)}</small></div></section><section class="strengths wrap"><article>{icon('users')}<h2>{S('Understand the user.','사용자 언어로 이해합니다.',lang)}</h2><p>{S('Firsthand facility engineering experience helps me translate field needs into workflows, validation rules and shared requirements.','현업 설비 엔지니어 경험으로 사용자의 요구를 업무 흐름·검증 규칙·합의 가능한 요구사항으로 정리합니다.',lang)}</p></article><article>{icon('code')}<h2>{S('Build across the stack.','기술의 경계를 연결합니다.',lang)}</h2><p>{S('Web applications, databases, drawing files, AWS storage and external APIs, connected around the real engineering workflow.','웹 애플리케이션·DB·도면 파일·AWS 스토리지·외부 API를 실제 엔지니어링 업무에 맞춰 연결합니다.',lang)}</p></article><article>{icon('deploy')}<h2>{S('Own what runs.','운영되는 결과를 책임집니다.',lang)}</h2><p>{S('CI/CD, Linux/Nginx, logs and incident resolution, with exception paths and recovery considered alongside feature delivery.','CI/CD·Linux·Nginx·로그·장애 대응을 담당하며 기능 구현과 함께 예외 경로·복구를 고려합니다.',lang)}</p></article></section><section class="work wrap" id="work"><div class="section-heading"><div><p class="eyebrow">01 / {S('SELECTED WORK','주요 프로젝트',lang)}</p><h2>{S('The problem. The build.','업무의 문제에서',lang)}<br><em>{S('The operational result.','실제 운영 결과까지.',lang)}</em></h2></div><p>{S('Four major platforms, followed by data operations and agent prototyping. Each project shows what changed and what I built.','주요 플랫폼 4개와 데이터 운영·에이전트 프로토타입입니다. 각 프로젝트에서 바뀐 업무와 직접 개발한 영역을 확인할 수 있습니다.',lang)}</p></div>'''
    s+=card(PROJECTS[0],lang,True)+'<div class="project-pair">'+card(PROJECTS[1],lang)+card(PROJECTS[2],lang)+'</div><div class="project-trio">'+''.join(card(p,lang) for p in PROJECTS[3:])+'</div></section>'
    s+=ai_section(lang,S,icon)
    s+=f'''<section class="about wrap" id="about"><div class="about-intro"><p class="eyebrow">03 / {S('EXPERIENCE & BACKGROUND','경력과 배경',lang)}</p><h2>Taekjun <em>(TJ)</em> Lee</h2><p class="about-lead">{S('Business systems and automation engineer at Samsung Electronics, Device Solutions.','삼성전자 DS부문에서 업무 시스템과 자동화를 다루는 엔지니어입니다.',lang)}</p><div class="timeline"><article><span>2019–2020</span><h3>{S('Facility Engineer','설비 엔지니어',lang)}</h3><p>{S('Built firsthand knowledge of utility operations and user workflows through equipment maintenance, monitoring-data analysis and anomaly investigations.','설비 유지보수·모니터링 데이터 분석·이상 조사를 수행하며 유틸리티 운영과 사용자 업무를 직접 이해했습니다.',lang)}</p></article><article><span>2020–{S('present','현재',lang)}</span><h3>{S('Systems Engineer','시스템 엔지니어',lang)}</h3><p>{S('Expanded from engineering data and process improvement into end-to-end system development.','엔지니어링 데이터·업무 프로세스 개선에서 시스템 전 과정 개발로 역할을 확장했습니다.',lang)}</p><ol class="career-growth"><li><strong>{S('Domain knowledge → data','도메인 이해 → 데이터',lang)}</strong><span>{S('Analysed and standardised engineering data to establish common master information.','엔지니어링 데이터 분석·표준화로 공통 기준정보를 정립했습니다.',lang)}</span></li><li><strong>{S('Data → process & system design','데이터 → 업무·시스템 설계',lang)}</strong><span>{S('Translated user workflows into requirements, process improvements and system operation.','사용자 업무를 요구사항·프로세스 개선·시스템 설계와 운영으로 연결했습니다.',lang)}</span></li><li><strong>{S('Design → development & delivery','설계 → 직접 개발·배포',lang)}</strong><span>{S('Took ownership of application development, databases, AWS delivery and production operations; coordinated vendors and delegated scoped tasks when project size required it.','애플리케이션·DB·AWS 배포·운영까지 전담하며, 프로젝트 규모에 따라 업체와 협업하고 후배에게 일부 업무를 배분했습니다.',lang)}</span></li></ol></article></div></div><div class="toolkit"><p class="eyebrow">{S('TECHNICAL TOOLKIT','주요 기술',lang)}</p><div><h3>{S('Applications','애플리케이션',lang)}</h3><p>Python · SQL · JavaScript · Java · FastAPI · Vue.js · Next.js · REST APIs</p></div><div><h3>{S('Cloud & delivery','클라우드·배포',lang)}</h3><p>AWS S3 · Lambda · EventBridge · SQS · CodeCommit · CodePipeline · CodeDeploy · Linux · Nginx · Git</p></div><div><h3>{S('Data & engineering platforms','데이터·엔지니어링 플랫폼',lang)}</h3><p>Oracle · ETL/EAI · Spotfire · ACC · Revit/BIM · Bedrock AgentCore · MES/MIS</p></div><div><h3>{S('Education','학력',lang)}</h3><p>{S('M.S. Industrial Engineering · Sungkyunkwan University · Feb 2026','산업공학 석사 · 성균관대학교 · 2026년 2월',lang)}<br>GPA 4.38/4.5</p><p class="thesis">{S('Thesis: Demand-Aware Pressure-Stable Screw Compressor Control Using Reinforcement Learning and XAI','논문: 강화학습과 XAI를 활용한 수요 대응형 압력 안정 스크류 컴프레서 제어',lang)}</p><p>{S('B.S. Mechanical Engineering · Sungkyunkwan University · Feb 2019','기계공학 학사 · 성균관대학교 · 2019년 2월',lang)}</p></div><div><h3>{S('Recognition & languages','수상·언어',lang)}</h3><p>{S('Samsung Best Contributor/Performer · 2022, 2023; project incentive awards · 2021–2024.','삼성 Best Contributor/Performer · 2022·2023; 프로젝트 인센티브 수상 · 2021–2024.',lang)}</p><p>{S('Korean: native · English: TOEFL iBT 107/120 (Apr 2025)','한국어: 모국어 · 영어: TOEFL iBT 107/120 (2025년 4월)',lang)}</p></div></div></section><section class="contact" id="contact"><div class="wrap"><p class="eyebrow">{S('LET’S CONNECT','함께 이야기해요',lang)}</p><h2>{S('Engineering context.','현장의 맥락을 이해하고',lang)}<br><em>{S('Software ownership.','소프트웨어를 책임집니다.',lang)}</em></h2><div class="contact-links"><a class="button light" href="mailto:leetj94@gmail.com">leetj94@gmail.com ↗</a><a href="https://www.linkedin.com/in/taek-jun-lee-a83160344" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="#home">{S('Back to top ↑','맨 위로 ↑',lang)}</a></div></div></section></main>'''
    return s+footer(lang)

def project(p,lang):
    prefix='../';slug=p['slug'];s=head(text(p['title'],lang),text(p['lead'],lang),lang,prefix,slug)+header(lang,prefix,slug,True)
    s+='<div class="case-layout wrap"><aside class="project-sidebar"><a class="back-link" href="../'+route('index',lang)+'#work">'+S('← All projects','← 전체 프로젝트',lang)+'</a><p class="mini-label">'+S('SELECTED WORK','주요 프로젝트',lang)+'</p><nav aria-label="'+S('Project navigation','프로젝트 메뉴',lang)+'">'
    for q in PROJECTS:s+='<a href="'+route(q['slug'],lang)+'" '+('aria-current="page"' if q['slug']==slug else '')+'><span>'+q['number']+'</span><span>'+text(q['title'],lang)+'</span></a>'
    s+='</nav><a class="sidebar-contact" href="mailto:leetj94@gmail.com">'+S('Discuss this work ↗','이 경험에 대해 이야기하기 ↗',lang)+'</a></aside><main id="main" class="case-main"><div class="breadcrumb"><a href="../'+route('index',lang)+'#work">'+S('Selected work','프로젝트',lang)+'</a><span>/ '+p['number']+'</span></div>'
    s+='<section class="case-hero"><div><div class="project-meta"><span>'+text(p['category'],lang)+'</span><span>'+p['period']+'</span></div><h1>'+text(p['title'],lang)+'</h1><p class="case-lead">'+text(p['lead'],lang)+'</p><p class="role-line"><span class="status-pill">'+text(p['status'],lang)+'</span>'+text(p['role'],lang)+'</p></div><figure class="case-art">'+art(p,lang,prefix)+'</figure></section>'
    if p['image']:s+='<p class="art-note">'+S('AI-generated concept illustration for understanding the workflow; not an actual system screenshot.','업무 흐름 이해를 돕기 위해 AI로 생성한 컨셉 이미지이며 실제 시스템 화면은 아닙니다.',lang)+'</p>'
    s+='<div class="case-metrics">'+''.join('<div><strong class="'+('long-metric' if len(v)>8 else '')+'">'+E(v)+'</strong><span>'+text(label,lang)+'</span></div>' for v,label in p['metrics'])+'</div>'
    s+='<nav class="case-jumps" aria-label="'+S('Case study sections','상세 페이지 목차',lang)+'">'+''.join('<a href="#'+ident+'">'+S(en,ko,lang)+' ↓</a>' for ident,en,ko in [('before-after','Before & after','개선 전후'),('system-flow','System flow','처리 흐름'),('my-build','What I built','개발 영역'),('results','Results','개선 결과')])+'</nav>'+disclosure(lang)
    s+='<section class="case-section" id="before-after"><p class="eyebrow">01 / '+S('WHAT CHANGED','무엇이 달라졌나',lang)+'</p><h2>'+S('The workflow, before and after.','업무 흐름의 개선 전후.',lang)+'</h2><div class="comparison">'
    for key,label,ic in [('before',S('BEFORE','개선 전',lang),'mail'),('after',S('AFTER','개선 후',lang),'check')]:
        graphic=''
        if slug=='document-automation':
            nodes=[('users','Supplier','납품 담당'),('users','Engineer','현업 담당'),('users','Reviewer','검토 담당')] if key=='before' else [('file','Submit','도면 제출'),('api','System','자동 처리'),('check','Review','결과 검토')]
            exchange='<svg viewBox="0 0 30 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 7h25m-5-4 5 4-5 4M28 18H3m5-4-5 4 5 4"/></svg>' if key=='before' else '<svg viewBox="0 0 30 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 12h25m-5-5 5 5-5 5"/></svg>'
            graphic='<div class="handover-visual">'+('<span class="handover-exchange">'+exchange+'</span>').join('<span class="handover-person">'+icon(n[0])+'<span>'+S(n[1],n[2],lang)+'</span></span>' for n in nodes)+'</div>'
        s+='<article class="compare-'+key+'"><div class="compare-label">'+icon(ic)+'<span>'+label+'</span></div><h3>'+text(p[key],lang)+'</h3>'+graphic+'<ol>'+''.join('<li><span>'+str(i+1)+'</span>'+text(step,lang)+'</li>' for i,step in enumerate(p[key+'_steps']))+'</ol><p>'+text(p[key+'_note'],lang)+'</p></article>'
    s+='</div></section><section class="case-section" id="system-flow"><p class="eyebrow">02 / '+S('TECHNOLOGY IN THE WORKFLOW','업무 흐름 속 기술',lang)+'</p><h2>'+S('Follow the information through the system.','정보가 시스템을 통과하는 과정.',lang)+'</h2><p class="section-intro">'+S('Select a stage to see its purpose, implementation technologies and operational safeguards.','단계를 선택하면 목적, 구현 기술, 운영상 보호 장치를 확인할 수 있습니다.',lang)+'</p><div class="interactive-flow" data-flow><ol class="system-flow">'
    for i,(ic,title,tech,description,safeguard) in enumerate(p['flow']):
        s+='<li><button type="button" data-flow-select="'+str(i)+'" aria-controls="flow-panel-'+str(i)+'" aria-pressed="'+str(i==0).lower()+'"><span class="stage-top"><span class="stage-number">0'+str(i+1)+'</span>'+icon(ic)+'</span><strong>'+text(title,lang)+'</strong><small>'+E(tech)+'</small></button></li>'
    s+='</ol><div class="flow-panels" aria-live="polite">'
    for i,(ic,title,tech,description,safeguard) in enumerate(p['flow']):
        s+='<article class="flow-panel" id="flow-panel-'+str(i)+'" data-flow-panel="'+str(i)+'" '+('hidden' if i else '')+'><div class="panel-heading">'+icon(ic)+'<h3>'+text(title,lang)+'</h3><span>'+E(tech)+'</span></div><p>'+text(description,lang)+'</p><div class="safeguard">'+icon('shield')+'<p>'+text(safeguard,lang)+'</p></div></article>'
    s+='</div></div></section><section class="case-section" id="my-build"><p class="eyebrow">03 / '+S('MY ENGINEERING OWNERSHIP','직접 개발한 영역',lang)+'</p><h2>'+S('What I designed, built and supported.','설계하고 개발하고 운영한 영역.',lang)+'</h2>'+tags(p)+'<div class="ownership-grid">'
    for ic,title,description in p['ownership']:s+='<article>'+icon(ic)+'<h3>'+text(title,lang)+'</h3><p>'+text(description,lang)+'</p></article>'
    s+='</div><div class="engineering-principle"><span class="mini-label">'+S('ENGINEERING JUDGMENT','설계의 핵심 판단',lang)+'</span><p>'+text(p['decision'],lang)+'</p></div><div class="checks"><span class="mini-label">'+S('EXCEPTION & VALIDATION FOCUS','예외·검증 시나리오',lang)+'</span><p>'+text(p['checks'],lang)+'</p></div></section><section class="case-section results" id="results"><p class="eyebrow">04 / '+S('OPERATIONAL RESULT','개선 결과',lang)+'</p><h2>'+S('What changed in practice.','실무에서 달라진 결과.',lang)+'</h2><p>'+text(p['result'],lang)+'</p>'
    if p.get('rollout'):s+='<aside class="project-rollout"><span class="mini-label">'+text(p['rollout'],lang)+'</span><p>'+text(p['rollout_note'],lang)+'</p></aside>'
    if p.get('estimate'):s+='<small>'+S('Productivity value estimates are based on workforce size, hourly pay and efficiency gains.','생산성 가치는 인원 규모·시간당 인건비·효율 개선을 기반으로 추정한 값입니다.',lang)+'</small>'
    nxt=PROJECTS[(PROJECTS.index(p)+1)%len(PROJECTS)]
    s+='</section><div class="case-pagination"><a href="../'+route('index',lang)+'#work">'+S('← All projects','← 전체 프로젝트',lang)+'</a><a href="'+route(nxt['slug'],lang)+'"><small>'+S('NEXT PROJECT','다음 프로젝트',lang)+'</small>'+text(nxt['title'],lang)+' ↗</a></div></main></div>'
    return s+footer(lang,prefix)

def write_page(stem,renderer):
    path=ROOT/stem;path.parent.mkdir(parents=True,exist_ok=True)
    path.with_suffix('.html').write_text(renderer('en'))
    path.with_name(path.name+'.en.html').write_text(renderer('en'))
    path.with_name(path.name+'.ko.html').write_text(renderer('ko'))

# The selected sidebar presentation is the only active HTML output.
# archive/v1 and version2*.html are historical snapshots; never regenerate them.
write_page('index',lambda lang:render_v2(lang,globals()))
print('Built the selected English/Korean portfolio and English alias.',ASSETS)
