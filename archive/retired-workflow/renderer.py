"""Retired walkthrough renderer; not imported by the active site."""
def render_explorer(lang,S):
    s='<article class="workflow-explorer" id="validation-workflow" data-validation-workflow><div class="explorer-heading"><span class="mini-label">'+S('INTERACTIVE WORKFLOW','직접 확인하는 처리 흐름',lang)+'</span><h3>'+S('Validate. Review. Deliver.','검증하고, 승인하고, 반영합니다.',lang)+'</h3><p>'+S('Run the checks, resolve the issues and inspect why approval and target delivery have separate states.','검수를 실행하고 오류를 조치한 뒤 승인과 대상별 연계 상태가 어떻게 분리되는지 확인할 수 있습니다.',lang)+'</p></div><noscript><p>'+S('Enable JavaScript to use the workflow controls.','처리 흐름을 확인하려면 JavaScript를 활성화해 주세요.',lang)+'</p></noscript><div class="explorer-controls">'
    for key,en,ko in [('validate','1 · Run checks','1 · 검수 실행'),('correct','2 · Correct & recheck','2 · 오류 수정·재검수'),('approve','3 · Approve revision','3 · 개정 승인'),('dispatch','4 · Deliver / retry','4 · 연계·재시도'),('reset','Reset','초기화')]:
        s+='<button type="button" data-workflow-action="'+key+'" '+('disabled' if key in ['correct','approve','dispatch'] else '')+'>'+S(en,ko,lang)+'</button>'
    s+='</div><div class="explorer-status" data-workflow-status aria-live="polite"></div><div class="explorer-records"><table><caption>'+S('Drawing records & validation','도면 레코드와 검증 결과',lang)+'</caption><thead><tr>'
    for en,ko in [('Drawing','도면'),('Asset','설비'),('Revision','개정'),('Check result','검수 결과')]:s+='<th scope="col">'+S(en,ko,lang)+'</th>'
    s+='</tr></thead><tbody data-workflow-records></tbody></table></div><div class="explorer-targets" data-workflow-targets></div><details class="explorer-log"><summary>'+S('Processing history','처리 이력',lang)+'</summary><ol data-workflow-log></ol></details></article>'
    return s
