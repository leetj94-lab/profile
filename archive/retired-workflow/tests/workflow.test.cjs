const test=require('node:test');
const assert=require('node:assert/strict');
const {create}=require('../workflow.js');
function approved(){let w=create();w.validate();w.correct();w.approve();return w;}
test('approval is blocked before a successful validation',()=>{let w=create();assert.equal(w.approve().approvedRevision,null);w.validate();assert.equal(w.approve().approvedRevision,null);});
test('validation identifies unknown assets and duplicate drawing revisions',()=>{let s=create().validate();assert.deepEqual(s.issues,[{index:1,rule:'UNKNOWN_ASSET'},{index:2,rule:'DUPLICATE_DRAWING'}]);assert.equal(s.status,'review-required');});
test('correction creates and validates a new revision with no stale approval',()=>{let w=create();w.validate();let s=w.correct();assert.equal(s.revision,2);assert.equal(s.validatedRevision,2);assert.equal(s.approvedRevision,null);assert.deepEqual(s.issues,[]);assert.equal(new Set(s.records.map(x=>x.drawing)).size,3);});
test('approval binds to the actual validated revision',()=>{let w=approved();let s=w.snapshot();assert.equal(s.approvedRevision,s.validatedRevision);assert.equal(s.status,'approved');});
test('delivery cannot run before approval',()=>{let w=create();w.validate();w.correct();assert.deepEqual(w.dispatch().targets.map(x=>x.attempts),[0,0]);});
test('partial delivery retains approval and separates target results',()=>{let w=approved();let s=w.dispatch();assert.equal(s.approvedRevision,2);assert.equal(s.status,'partial-delivery');assert.deepEqual(s.targets.map(x=>x.state),['delivered','retry-required']);});
test('retry sends only the failed target and final delivery is idempotent',()=>{let w=approved();w.dispatch();let s=w.dispatch();assert.equal(s.status,'delivered');assert.deepEqual(s.targets.map(x=>x.attempts),[1,2]);assert.deepEqual(w.dispatch(),s);});
test('approval freezes the reviewed revision from correction and revalidation',()=>{let w=approved();let s=w.snapshot();assert.deepEqual(w.correct(),s);assert.deepEqual(w.validate(),s);});
test('reset clears approval, validation and delivery attempts',()=>{let w=approved();w.dispatch();let s=w.reset();assert.equal(s.approvedRevision,null);assert.equal(s.validatedRevision,null);assert.equal(s.revision,1);assert.deepEqual(s.targets.map(x=>x.attempts),[0,0]);});
