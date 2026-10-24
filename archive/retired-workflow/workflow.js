/* Deterministic validation and delivery state, shared by the explorer and tests. */
(function (root, factory) {
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.PortfolioWorkflow=api;
  if(typeof document!=='undefined')api.mount(document);
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const seed=()=>[{drawing:'DR-101',asset:'P-101',revision:1},{drawing:'DR-102',asset:'P-999',revision:1},{drawing:'DR-101',asset:'P-103',revision:1}];
  const master=new Set(['P-101','P-102','P-103']);
  function create(){
    let s;
    const reset=()=>{s={records:seed(),revision:1,validatedRevision:null,approvedRevision:null,issues:[],status:'received',targets:[{id:'A',state:'pending',attempts:0},{id:'B',state:'pending',attempts:0}],events:['received']};return snapshot();};
    const snapshot=()=>JSON.parse(JSON.stringify(s));
    const validate=()=>{
      if(s.approvedRevision!==null)return snapshot();
      const keys=new Set();s.issues=[];
      s.records.forEach((r,index)=>{let key=r.drawing+':'+r.revision;
        if(!master.has(r.asset))s.issues.push({index,rule:'UNKNOWN_ASSET'});
        if(keys.has(key))s.issues.push({index,rule:'DUPLICATE_DRAWING'});
        keys.add(key);
      });
      s.validatedRevision=s.revision;s.status=s.issues.length?'review-required':'validated';s.events.push(s.status);return snapshot();
    };
    const correct=()=>{
      if(!s.issues.length||s.approvedRevision!==null)return snapshot();
      s.revision++;s.records=seed().map((r,i)=>({...r,asset:'P-10'+(i+1),drawing:'DR-10'+(i+1),revision:s.revision}));
      s.validatedRevision=null;s.approvedRevision=null;s.status='received';s.events.push('revision-created');return validate();
    };
    const approve=()=>{
      if(s.status!=='validated'||s.issues.length||s.validatedRevision!==s.revision)return snapshot();
      s.approvedRevision=s.revision;s.status='approved';s.events.push('approved');return snapshot();
    };
    const dispatch=()=>{
      if(s.approvedRevision!==s.revision||s.approvedRevision===null)return snapshot();
      let changed=false;
      s.targets.forEach(t=>{if(t.state==='delivered')return;changed=true;t.attempts++;t.state=t.id==='B'&&t.attempts===1?'retry-required':'delivered';});
      if(!changed)return snapshot();
      s.status=s.targets.every(t=>t.state==='delivered')?'delivered':'partial-delivery';s.events.push(s.status);return snapshot();
    };
    reset();return {snapshot,reset,validate,correct,approve,dispatch};
  }
  function mount(doc){
    const ko=doc.documentElement.lang==='ko';const T=(en,kr)=>ko?kr:en;
    const labels={received:T('Received','접수'), 'review-required':T('Review required','오류 조치 필요'),validated:T('Validated','검증 완료'),approved:T('Approved','승인 완료'),'partial-delivery':T('Partial delivery · retry B','일부 연계 완료 · B 재시도 필요'),delivered:T('Delivered','연계 완료'),'retry-required':T('Retry required','재시도 필요'),pending:T('Pending','대기'),'revision-created':T('New revision created','새 개정 생성')};
    const rules={UNKNOWN_ASSET:T('Unknown asset ID','기준정보에 없는 설비 ID'),DUPLICATE_DRAWING:T('Duplicate drawing/revision','도면·개정 중복')};
    doc.querySelectorAll('[data-validation-workflow]').forEach(el=>{
      const engine=create();const buttons=[...el.querySelectorAll('[data-workflow-action]')];
      const cell=(value,tag='td')=>{const n=doc.createElement(tag);n.textContent=value;return n;};
      function render(){const s=engine.snapshot();
        el.querySelector('[data-workflow-status]').textContent=T('Revision ','개정 ')+s.revision+' · '+labels[s.status]+(s.approvedRevision!==null?' · '+T('Approved revision ','승인 개정 ')+s.approvedRevision:'');
        const rows=el.querySelector('[data-workflow-records]');rows.replaceChildren();
        s.records.forEach((r,i)=>{let tr=doc.createElement('tr');let issues=s.issues.filter(x=>x.index===i);let result=s.validatedRevision===null?T('Not checked','검수 전'):issues.length?issues.map(x=>rules[x.rule]).join(' · '):T('Passed','통과');
          tr.dataset.result=issues.length?'error':s.validatedRevision!==null?'passed':'pending';[r.drawing,r.asset,r.revision,result].forEach(v=>tr.appendChild(cell(v)));rows.appendChild(tr);});
        const targets=el.querySelector('[data-workflow-targets]');targets.replaceChildren();
        s.targets.forEach(t=>{let card=doc.createElement('div');card.dataset.deliveryState=t.state;card.appendChild(cell(T('Target ','대상 ')+t.id,'strong'));card.appendChild(cell(labels[t.state],'span'));card.appendChild(cell(T('Send attempts: ','전송 시도: ')+t.attempts,'small'));targets.appendChild(card);});
        const log=el.querySelector('[data-workflow-log]');log.replaceChildren();s.events.forEach((key,i)=>log.appendChild(cell(String(i+1).padStart(2,'0')+' · '+labels[key],'li')));
        buttons.forEach(b=>{let k=b.dataset.workflowAction;b.disabled=k==='correct'?s.issues.length===0||s.approvedRevision!==null:k==='approve'?s.status!=='validated':k==='dispatch'?s.approvedRevision===null||s.status==='delivered':k==='validate'?s.approvedRevision!==null:false;});
      }
      buttons.forEach(b=>b.addEventListener('click',()=>{engine[b.dataset.workflowAction]();render();}));render();
    });
  }
  return {create,mount};
});
