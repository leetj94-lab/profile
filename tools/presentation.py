"""AI practice copy and the selected sidebar presentation."""
import re
from engineering import render_operations

def ai_section(lang,S,icon):
    s=f'''<section class="ai-section" id="approach"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">02 / {S('AI ENGINEERING PHILOSOPHY','AI 활용 철학',lang)}</p><h2>{S('AI changes how we build.','AI가 바꾼 개발 방식.',lang)}<br><em>{S('Expertise shapes the quality.','품질을 결정하는 전문성.',lang)}</em></h2></div><p>{S('I believe AI has changed the way systems are developed. Code generation is widely accessible, but the quality of the result still depends on domain knowledge, engineering experience and the standards we apply.','AI로 시스템 개발의 패러다임이 바뀌었다고 생각합니다. 누구나 코드를 생성할 수 있는 환경에서도 결과의 품질은 도메인 이해, 엔지니어링 경험, 적용하는 기준에 따라 달라집니다.',lang)}</p></div><p class="ai-thesis">{S('I use AI to turn engineering judgment into a repeatable team practice: define the problem, agree on standards, generate within those boundaries, then review and verify.','AI를 활용해 엔지니어링 판단을 팀이 반복 적용할 수 있는 방식으로 만듭니다. 문제를 정의하고, 표준을 정하고, 그 기준 안에서 코드를 생성한 뒤 검토하고 검증합니다.',lang)}</p><div class="ai-pillars">'''
    pillars=[
      ('users','01','Context before generation','생성 전에 업무 맥락부터','My field and software experience helps me define the user’s problem, system boundaries and expected behavior before asking AI to implement a solution.','현업과 개발 경험을 바탕으로 사용자의 문제, 시스템 경계, 기대 동작을 먼저 정리한 뒤 AI에 구현을 요청합니다.'),
      ('code','02','Shared team standards','팀이 공유하는 개발 표준','I encode coding patterns, naming, API contracts, UI conventions and error-handling rules in SKILL.md. Different teammates using AI can work toward the same patterns and standards.','코딩 패턴, 명명 규칙, API 계약, UI 기준, 오류 처리 규칙을 SKILL.md에 정리합니다. 팀 내 다른 사람이 AI를 사용해도 유사한 패턴과 동일한 표준을 따르도록 합니다.'),
      ('database','03','Code others can maintain','공유·유지보수·재사용 가능한 코드','Clear interfaces, modular responsibilities and reusable patterns help generated code fit a shared codebase, support collaboration and remain adaptable as requirements change.','명확한 인터페이스, 모듈별 책임, 재사용 가능한 패턴을 정해 생성 코드가 공통 코드베이스에 어울리고 협업과 요구사항 변경에도 대응하도록 합니다.'),
      ('shield','04','Verification designed upfront','미리 정의하는 기능·테스트 기준','I define functional acceptance criteria and test scenarios before generation, including boundaries, exceptions and recovery. Generated code must have behavior that can be inspected and tested.','코드 생성 전에 기능 수용 기준과 경계 조건·예외·복구 테스트 시나리오를 정의합니다. 생성된 코드가 이후에도 동작을 확인하고 테스트할 수 있는 구조를 갖추도록 합니다.')]
    for ic,no,en,ko,bodyen,bodyko in pillars:
        s+='<article><div class="pillar-top">'+icon(ic)+'<span>'+no+'</span></div><h3>'+S(en,ko,lang)+'</h3><p>'+S(bodyen,bodyko,lang)+'</p></article>'
    s+='</div><div class="ai-standard"><div><span class="mini-label">SKILL.md</span><h3>'+S('Reusable instructions for a shared engineering contract.','공통 개발 기준을 재사용하는 지침.',lang)+'</h3><p>'+S('The skill recipes make the rules explicit: UI design, code structure and test generation follow predefined expectations across contributors and AI-assisted tasks.','스킬 레시피는 팀의 규칙을 명시하는 장치입니다. UI 디자인·코드 구조·테스트 생성이 작업자와 AI 활용 작업 전반에서 사전 정의한 기준을 따르도록 합니다.',lang)+'</p></div><div class="ai-skill-files"><code>ui-design/SKILL.md</code><code>coding-standards/SKILL.md</code><code>test-generation/SKILL.md</code></div></div><ol class="ai-method">'
    for en,ko in [('Understand','업무 이해'),('Define standards','기준 정의'),('Generate','코드 생성'),('Review','결과 검토'),('Verify','동작 검증')]:s+='<li>'+S(en,ko,lang)+'</li>'
    s+='</ol><p class="ai-note">'+S('My goal is to improve team consistency, reliability, maintainability and delivery quality through AI—not just save individual effort. I retain responsibility for the engineering decisions and review of generated results. This portfolio also uses AI-assisted design and development.','AI를 통해 개인의 작업 편의뿐 아니라 팀의 일관성, 신뢰성, 유지보수성, 개발 품질을 높이는 것이 목표입니다. 엔지니어링 판단과 생성 결과의 검토는 제가 책임집니다. 이 포트폴리오의 디자인·개발에도 AI를 활용했습니다.',lang)+'</p></div></section>'
    return s

def render_v2(lang,c):
    S,icon,text,route=c['S'],c['icon'],c['text'],c['route']
    P=c['PROJECTS']; assets=c['ASSETS'];year=c['YEAR']
    s=c['head'](S('Portfolio · Quick view','포트폴리오 · 빠른 탐색',lang),S('A concise view of TJ Lee’s systems delivery, projects, AI engineering approach and experience.','TJ Lee의 시스템 개발, 프로젝트, AI 활용 철학과 경력을 빠르게 살펴보는 포트폴리오.',lang),lang,'','index')
    s=s.replace('</head>','<link rel="stylesheet" href="'+assets['v2-styles']+'"></head>').replace('<body>','<body class="v2-page" data-version="2">')
    sections=[('home','screen','Overview','개요'),('work','code','Projects','프로젝트'),('approach','spark','AI philosophy','AI 활용 철학'),('about','users','Experience','경력'),('contact','mail','Contact','연락처')]
    s+='<aside class="v2-rail"><a class="wordmark" href="#home"><span class="monogram">tj.</span><span>TJ LEE<small>SYSTEMS & AUTOMATION</small></span></a><p class="v2-rail-caption">'+S('SYSTEMS & AUTOMATION','시스템 개발 · 자동화',lang)+'</p><nav class="v2-nav" aria-label="'+S('Main navigation','주 메뉴',lang)+'">'
    for ident,ic,en,ko in sections:s+='<a href="#'+ident+'" data-v2-nav="'+ident+'" '+('aria-current="page"' if ident=='home' else '')+'>'+icon(ic)+'<span>'+S(en,ko,lang)+'</span></a>'
    s+='</nav><nav class="v2-subnav" aria-label="'+S('Project navigation','프로젝트 메뉴',lang)+'" hidden>'
    short={'asset-master-data':('Master data','기준정보·연계'),'drawing-information':('Drawing context','도면·공간 정보'),'digital-twin':('3D digital twin','3D 디지털 트윈'),'document-automation':('Document delivery','도면 납품·갱신'),'operations-analytics':('Data operations','데이터 운영'),'engineering-agents':('Agent prototypes','에이전트 실험')}
    for p in P:
        en,ko=short[p['slug']]
        s+='<a href="#project-'+p['slug']+'" data-v2-project="'+p['slug']+'"><span>'+p['number']+'</span>'+S(en,ko,lang)+'</a>'
    s+='</nav><div class="v2-rail-bottom"><div class="language-switch" role="group" aria-label="'+S('Language selection','언어 선택',lang)+'"><a href="index.en.html" data-site-lang="en" lang="en" '+('aria-current="true"' if lang=='en' else '')+'>EN</a><a href="index.ko.html" data-site-lang="ko" lang="ko" '+('aria-current="true"' if lang=='ko' else '')+'>한국어</a></div><a class="v2-email" href="mailto:leetj94@gmail.com">leetj94@gmail.com ↗</a></div></aside><div class="v2-content"><div class="v2-topbar"><span>TJ LEE / <span data-v2-current>'+S('Overview','개요',lang)+'</span></span><span>'+S('Business Systems & Automation Engineer','업무 시스템 · 자동화 엔지니어',lang)+'</span></div><main id="main" class="v2-main" tabindex="-1"><h1 class="sr-only">'+S('TJ Lee — Portfolio','TJ Lee — 포트폴리오',lang)+'</h1><section class="v2-panel v2-overview" id="home" data-v2-panel="home" data-v2-label="'+S('Overview','개요',lang)+'"><p class="eyebrow">SAMSUNG ELECTRONICS · TAEKJUN (TJ) LEE</p><h2 class="v2-title">'+S('Business systems.','현업을 이해하는',lang)+'<br><em>'+S('Built end to end.','시스템 개발자.',lang)+'</em></h2><p class="v2-lead">'+S('A field engineer turned software developer. I connect user needs, full-stack development, AWS delivery and production operations.','현업 엔지니어 경험을 가진 개발자입니다. 사용자 요구부터 풀스택 개발, AWS 배포와 운영까지 연결합니다.',lang)+'</p><div class="v2-profile-strip"><span>'+S('Systems Engineer · Samsung Electronics ·','삼성전자 시스템 엔지니어 ·',lang)+' <strong data-career-years>'+str(year-2019)+'+</strong> '+S('years','년 경력',lang)+'</span><span>'+S('End-to-end ownership across design, development and operations.','설계부터 개발·운영까지 프로젝트 전 과정을 담당합니다.',lang)+'</span></div><div class="v2-strength-grid">'
    strengths=[('users','Engineering insight','현업을 이해하는 개발','Turn firsthand operational experience into practical software requirements.','직접 시스템을 사용했던 경험을 실질적인 요구사항으로 연결합니다.','asset-master-data'),('code','Full-stack delivery','풀스택 구현 역량','Connect web applications, databases, AWS and engineering APIs.','웹·DB·AWS·엔지니어링 API를 연결해 시스템을 구현합니다.','document-automation'),('deploy','Production ownership','운영까지 이어지는 책임','Build for deployment, exception handling and ongoing operations.','배포·예외 처리·지속적인 운영까지 고려해 개발합니다.','operations-analytics')]
    for ic,en,ko,bodyen,bodyko,slug in strengths:s+='<a href="#project-'+slug+'">'+icon(ic)+'<h3>'+S(en,ko,lang)+'</h3><p>'+S(bodyen,bodyko,lang)+'</p><small>'+S('See it in practice ↗','적용 사례 보기 ↗',lang)+'</small></a>'
    s+='</div><p class="v2-core-stack">Python / FastAPI · Vue.js · SQL / Oracle · AWS · Linux / CI/CD</p><div class="v2-section-row"><h3>'+S('From shared foundations to current data','공통 기반부터 지속적인 데이터 갱신까지',lang)+'</h3><a href="#work">'+S('All six projects →','전체 프로젝트 6개 →',lang)+'</a></div><div class="v2-project-grid">'
    def v2card(p):
        return '<a class="v2-project-card" href="#project-'+p['slug']+'"><div class="v2-card-art">'+c['art'](p,lang)+('<span class="v2-image-credit" title="'+S('AI-generated illustration','AI 생성 이미지',lang)+'">AI</span>' if p['image'] else '')+'</div><div><span class="v2-card-stage">'+p['number']+' / '+text(p['story_stage'],lang)+'</span><span class="v2-card-meta">'+p['period']+' · '+text(p['status'],lang)+'</span><h3>'+text(p['title'],lang)+'</h3><p>'+text(p['summary'],lang)+'</p><span class="v2-card-action">'+S('Read case study ↗','상세 내용 보기 ↗',lang)+'</span></div></a>'
    s+=''.join(v2card(p) for p in [P[0],P[3]])+'</div><div class="v2-overview-note">'+icon('spark')+'<p>'+S('AI-assisted delivery, guided by shared standards and engineering judgment.','팀의 표준과 엔지니어링 판단을 기반으로 AI를 활용합니다.',lang)+'</p><a href="#approach">'+S('My approach →','활용 철학 →',lang)+'</a></div><a class="workflow-entry" href="#project-document-automation-validation-workflow">'+S('Explore validation & delivery behavior →','검수·승인·연계 흐름 직접 확인하기 →',lang)+'</a></section><section class="v2-panel" id="work" data-v2-panel="work" data-v2-label="'+S('Projects','프로젝트',lang)+'" hidden><p class="eyebrow">'+S('SELECTED SYSTEMS & AUTOMATION','시스템 개발 · 자동화',lang)+'</p><h2 class="v2-title">'+S('One foundation. Connected systems.','하나의 기반에서 연결된 시스템으로.',lang)+'</h2><p class="v2-lead">'+S('Each platform addressed the next information gap: shared asset data, drawing context, connected 3D models, then a faster and richer update cycle.','각 플랫폼은 앞선 단계에서 드러난 정보의 공백을 해결했습니다. 기준정보에서 도면·공간 정보, 3D 연계, 신속하고 풍부한 데이터 갱신으로 확장했습니다.',lang)+'</p><nav class="project-journey" aria-label="'+S('Platform development journey','플랫폼 발전 흐름',lang)+'">'+''.join('<a href="#project-'+p['slug']+'"><small>'+p['number']+' · '+p['period']+'</small><strong>'+text(p['story_stage'],lang)+'</strong><span>↗</span></a>' for p in P[:4])+'</nav><div class="v2-project-grid">'+''.join(v2card(p) for p in P[:4])+'</div><div class="parallel-heading"><p class="eyebrow">'+S('PARALLEL IMPROVEMENT & EXPLORATION','병행 개선과 확장 실험',lang)+'</p><h3>'+S('Improve operations. Explore what comes next.','운영을 개선하고, 다음 가능성을 실험합니다.',lang)+'</h3><p>'+S('Alongside the platforms: data and operational automation across projects, plus engineering-agent prototypes.','플랫폼 개발과 병행한 데이터·운영 자동화, 그리고 엔지니어링 에이전트 프로토타입입니다.',lang)+'</p></div><div class="v2-project-grid">'+''.join(v2card(p) for p in P[4:])+'</div></section>'
    original=c['home'](lang)
    for ident,pattern,en,ko in [('approach',r'<section class="ai-section" id="approach">.*?</section>','AI philosophy','AI 활용 철학'),('about',r'<section class="about wrap" id="about">.*?</section>','Experience','경력'),('contact',r'<section class="contact" id="contact">.*?</section>','Contact','연락처')]:
        block=re.search(pattern,original,re.S).group()
        block=block.replace('<section ', '<section data-v2-panel="'+ident+'" data-v2-label="'+S(en,ko,lang)+'" hidden ',1)
        if ident=='about':
            jumps='<nav class="experience-jumps" aria-label="'+S('Experience sections','경력 목차',lang)+'"><a href="#career-path">'+S('Career progression ↓','경력 발전 과정 ↓',lang)+'</a><a href="#mes-operations">'+S('MES/MIS & business improvement ↓','MES/MIS·업무 개선 ↓',lang)+'</a></nav>'
            block=block.replace('<div class="timeline">',jumps+'<div class="timeline" id="career-path">')
            block=block.replace('</section>',render_operations(lang,S,icon)+'</section>')
        s+=block
    for p in P:
        key='project-'+p['slug']; rendered=c['project'](p,lang)
        body=rendered.split('<main id="main" class="case-main">',1)[1].split('</main></div>',1)[0]
        body=body.replace('../'+route('index',lang)+'#work','#work').replace('src="../assets/','src="assets/')
        # Keep hiring evidence visible before optional stage exploration.
        sections=list(re.finditer(r'<section class="case-section[^"]*" id="([^"]+)">.*?</section>',body,re.S))
        assert len(sections)==5
        parts={m[1]:m[0] for m in sections}
        reading_order=['before-after','results','my-build','system-flow','engineering']
        ordered=[]
        for no,ident in enumerate(reading_order,1):
            ordered.append(re.sub(r'(<p class="eyebrow">)\d{2} /',lambda m:m[1]+f'{no:02} /',parts[ident],count=1))
        body=body[:sections[0].start()]+''.join(ordered)+body[sections[-1].end():]

        for other in P:body=body.replace('href="'+route(other['slug'],lang)+'"','href="#project-'+other['slug']+'"')
        for attr in ['id','aria-controls']:
            body=re.sub(r'\b'+attr+r'="([^"]+)"',lambda m:attr+'="'+key+'-'+m[1]+'"',body)
        body=re.sub(r'href="#(?!work")([^"]+)"',lambda m:'href="#'+key+'-'+m[1]+'"' if not m[1].startswith('project-') else m[0],body)
        # The app has one document h1; panel headings retain a coherent hierarchy.
        body=body.replace('<h3','<h4').replace('</h3>','</h4>').replace('<h2','<h3').replace('</h2>','</h3>').replace('<h1>','<h2 class="case-title">').replace('</h1>','</h2>')
        context='<aside class="project-context"><span class="mini-label">'+text(p['story_stage'],lang)+'</span><p>'+text(p['story_context'],lang)+'</p></aside>'
        marker='<section class="case-hero">'
        body=body.replace(marker,context+marker)
        s+='<section class="v2-panel v2-case" id="'+key+'" data-v2-panel="'+key+'" data-v2-label="'+text(p['title'],lang)+'" hidden>'+body+'</section>'
    s+='</main><noscript><style>[data-v2-panel][hidden]{display:block!important}</style><p class="v2-noscript">'+S('JavaScript is unavailable. All sections are shown below their navigation links.','JavaScript를 사용할 수 없어 모든 섹션을 함께 표시합니다.',lang)+'</p></noscript>'
    end=c['footer'](lang).replace('</body>','<script src="'+assets['v2-script']+'"></script><script src="'+assets['workflow']+'"></script></body>')
    return s+end.replace('<footer','</div><footer',1)
