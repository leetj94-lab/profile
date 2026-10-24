"""Bilingual engineering detail components for the active portfolio only."""
def render_engineering(p,lang,S,text,icon):
    e=p['engineering']
    s='<section class="case-section engineering-depth" id="engineering"><p class="eyebrow">04 / '+S('DECISIONS & RELIABILITY','기술 판단과 신뢰성',lang)+'</p><h2>'+S('The constraints behind the implementation.','구현을 결정한 문제와 판단.',lang)+'</h2><div class="engineering-decisions">'
    for i,d in enumerate(e['decisions'],1):
        s+='<article><span class="decision-number">0'+str(i)+'</span><h3>'+text(d['title'],lang)+'</h3><dl>'
        for key,en,ko in [('challenge','Challenge','난관'),('choice','Decision','결정'),('reason','Why this approach','선택 이유')]:
            s+='<div><dt>'+S(en,ko,lang)+'</dt><dd>'+text(d[key],lang)+'</dd></div>'
        s+='</dl></article>'
    s+='</div><div class="recovery-map"><h3>'+S('Explicit states. Recoverable work.','명확한 상태, 복구 가능한 작업.',lang)+'</h3><ol class="recovery-states">'
    for state in e['states']:s+='<li>'+text(state,lang)+'</li>'
    s+='</ol><p>'+icon('shield')+text(e['recovery'],lang)+'</p></div><details class="verification-detail"><summary>'+icon('check')+'<span>'+S('Verification cases & expected behavior','검증 사례와 기대 동작',lang)+'</span><span class="detail-count">'+str(len(e['verification']))+'</span></summary><div class="verification-body"><table><caption class="sr-only">'+S('Boundary and recovery checks','경계·복구 검증',lang)+'</caption><thead><tr><th scope="col">'+S('Condition','조건',lang)+'</th><th scope="col">'+S('Expected behavior','기대 동작',lang)+'</th></tr></thead><tbody>'
    for v in e['verification']:s+='<tr><th scope="row">'+text(v['condition'],lang)+'</th><td>'+text(v['expected'],lang)+'</td></tr>'
    return s+'</tbody></table></div></details></section>'

def render_operations(lang,S,icon):
    s='<article class="mes-operations" id="mes-operations"><div class="mes-heading"><p class="eyebrow">MES / MIS</p><h3>'+S('Operations that become better systems.','운영의 경험을 시스템 개선으로.',lang)+'</h3><p>'+S('Alongside project development, I operated MES/MIS services, answered user enquiries and turned recurring pain points into cross-functional improvement work.','프로젝트 개발과 함께 MES/MIS 운영과 사용자 문의 대응을 담당하고, 반복되는 불편을 부서 간 개선 과제로 구체화했습니다.',lang)+'</p></div><ol class="mes-process">'
    rows=[('users','Listen & identify','의견 수렴·과제 발굴','Used regular stakeholder forums, system VoC and user enquiries to distinguish defects, process gaps and enhancement requests.','정기 협의체·시스템 VoC·사용자 문의에서 오류, 업무 절차의 공백, 기능 개선 요구를 구분했습니다.'),('search','Assess the impact','현장 확인·영향 분석','Visited affected departments to trace user workflows, data dependencies and the systems touched by a proposed change.','관련 부서를 방문해 실제 업무 흐름, 데이터 의존성, 변경에 영향을 받는 시스템을 확인했습니다.'),('drawing','Design the change','업무·시스템 상세 설계','Defined business and system process flows, exception paths, responsibilities and acceptance criteria for major improvements.','큰 개선 과제의 업무·시스템 프로세스, 예외 경로, 담당 범위와 수용 기준을 상세 설계했습니다.'),('deploy','Coordinate & verify','적용 조율·결과 확인','Aligned implementation scope with users and delivery teams, coordinated vendors where needed and checked whether the change resolved the original issue.','사용자·구현 담당자와 범위를 합의하고 필요한 경우 업체와 조율하며, 적용 결과가 최초 문제를 해결했는지 확인했습니다.')]
    for i,(ic,en,ko,bodyen,bodyko) in enumerate(rows,1):
        s+='<li><div>'+icon(ic)+'<span>0'+str(i)+'</span></div><h4>'+S(en,ko,lang)+'</h4><p>'+S(bodyen,bodyko,lang)+'</p></li>'
    s+='</ol><details class="mes-example"><summary>'+S('An improvement from request to acceptance','요청을 설계·검증으로 연결한 개선 사례',lang)+'</summary><p>'+S('For an equipment-lifecycle change, I mapped the departments creating, modifying and consuming asset records; analysed the impact on existing work orders and interfaces; and defined process changes and acceptance scenarios before implementation.','설비 생애주기 변경 과제에서는 설비 정보를 생성·수정·활용하는 부서를 연결하고, 기존 작업 이력과 인터페이스의 영향 범위를 분석한 뒤 구현 전에 변경 프로세스와 수용 시나리오를 정리했습니다.',lang)+'</p><p>'+S('Acceptance covered new records, historical references, rejected changes and failed integrations—connecting the user’s request to behavior that could be checked.','신규 등록, 과거 이력 참조, 변경 반려, 연계 실패를 수용 기준에 포함해 사용자의 요구를 확인 가능한 시스템 동작으로 구체화했습니다.',lang)+'</p></details></article>'
    return s
