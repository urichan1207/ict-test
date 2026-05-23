import re, json
from pathlib import Path

html_file = Path(r'C:\Users\natuk\Downloads\ICT認定テスト_改訂版_全レベル_2.html')
with open(html_file, 'r', encoding='utf-8') as f:
    original = f.read()

data_js = re.search(r'const\s+DATA\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
lv_js = re.search(r'const\s+LV\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
pass_js = re.search(r'const\s+PASS\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
kanten_js = re.search(r'const\s+KANTEN\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#1A2A22;--ink2:#4A5A52;--ink3:#8A9A92;--bg:#F4F7F5;--card:#FFF;--line:#E2E8E4;
--green:#1D9E75;--green-d:#0F6E56;--green-l:#E1F5EE;--gold:#BA7517;--gold-l:#FAEEDA;--red:#D85A30;--red-l:#FAECE7}
body{font-family:'Noto Sans JP',sans-serif;background:var(--bg);color:var(--ink);line-height:1.8;-webkit-font-smoothing:antialiased}
ruby rt{font-size:.5em;color:var(--ink3);font-weight:400}
.app{max-width:900px;margin:0 auto;padding:24px 16px 70px}
.hd{text-align:center;margin-bottom:20px}
.hd h1{font-size:clamp(18px,4vw,26px);font-weight:900;letter-spacing:.03em;color:var(--green-d)}
.hd p{font-size:12.5px;color:var(--ink3);margin-top:6px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:14px;font-size:13px;color:var(--ink2)}
.intro b{color:var(--ink)}.intro .src{font-size:11px;color:var(--ink3);margin-top:8px}
.banner{background:var(--green-l);border:1px solid #9BD9C4;border-radius:12px;padding:13px 16px;margin-bottom:20px;font-size:12.5px;color:var(--green-d);line-height:1.7}
.banner b{font-weight:700}
.lv-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
@media(max-width:680px){.lv-grid{grid-template-columns:1fr 1fr}}
@media(max-width:460px){.lv-grid{grid-template-columns:1fr}}
.lv-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;cursor:pointer;transition:transform .15s,box-shadow .15s;border-top:4px solid var(--c)}
.lv-card:hover{transform:translateY(-3px);box-shadow:0 10px 26px rgba(0,0,0,.09)}
.lv-tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--c);border-radius:18px;padding:3px 11px;margin-bottom:9px}
.lv-name{font-size:16px;font-weight:700;margin-bottom:3px}
.lv-grade{font-size:11.5px;color:var(--ink2);font-weight:500;margin-bottom:8px;line-height:1.5}
.lv-desc{font-size:11.5px;color:var(--ink2);line-height:1.55;margin-bottom:8px}
.lv-foot{font-size:10.5px;color:var(--ink3);border-top:1px dashed var(--line);padding-top:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px}
.lv-pass{font-weight:700;color:var(--c)}
.quiz,.result{display:none}.quiz.on,.result.on{display:block}
.qbar{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.qback{font-size:13px;color:var(--ink2);background:none;border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer}
.qback:hover{background:var(--line)}
.qprog{flex:1;min-width:140px}.qprog-t{font-size:12px;color:var(--ink3);margin-bottom:4px}
.qprog-b{height:6px;background:var(--line);border-radius:3px;overflow:hidden}
.qprog-f{height:100%;background:var(--green);border-radius:3px;transition:width .3s}
.qcard{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;margin-bottom:14px}
.qk{display:inline-block;font-size:11px;font-weight:700;color:#fff;border-radius:6px;padding:3px 10px;margin-bottom:6px}
.qlink{font-size:10.5px;color:var(--ink3);margin-bottom:13px;line-height:1.5}
.qlink b{color:var(--ink2);font-weight:500}
.qintro{font-size:14px;margin-bottom:13px;line-height:1.85}
.qcond{background:#FFF9EC;border-left:3px solid var(--gold);border-radius:8px;padding:11px 14px;margin-bottom:13px;font-size:13px;line-height:1.8}
.qcond div{margin:2px 0}
.qlist{background:var(--bg);border-radius:8px;padding:11px 16px;margin-bottom:13px;font-size:13px;line-height:1.9}
.qlist div{margin:1px 0}
.qsteps{counter-reset:s;margin-bottom:13px}
.qsteps div{background:var(--bg);border-radius:6px;padding:8px 12px;margin-bottom:5px;font-size:13px}
.qtable{width:100%;border-collapse:collapse;margin-bottom:13px;font-size:12.5px;overflow:hidden;border-radius:8px}
.qtable th{background:var(--green-d);color:#fff;padding:8px 10px;font-weight:500;text-align:left;font-size:12px}
.qtable td{padding:7px 10px;border-bottom:1px solid var(--line);background:var(--card)}
.qtable tr:last-child td{border-bottom:none}
.qtable tr:nth-child(even) td{background:#FAFBFA}
.qcode{background:#1E2A24;color:#D8E8E0;border-radius:10px;padding:14px 16px;margin-bottom:13px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;line-height:1.85;white-space:pre-wrap;overflow-x:auto}
.qcode ruby rt{color:#7FA894}
.qt{font-size:15.5px;font-weight:700;margin-bottom:16px;line-height:1.7}
.choices{display:flex;flex-direction:column;gap:9px}
.ch{display:flex;align-items:flex-start;gap:11px;background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:12px 15px;cursor:pointer;transition:all .15s;font-size:14px;text-align:left;line-height:1.7}
.ch:hover{border-color:var(--green);background:var(--green-l)}
.ch.sel{border-color:var(--green);background:var(--green-l)}
.ch.correct{border-color:var(--green);background:var(--green-l)}
.ch.wrong{border-color:var(--red);background:var(--red-l)}.ch.dim{opacity:.5}
.ch-m{flex-shrink:0;width:24px;height:24px;border-radius:50%;border:1.5px solid var(--ink3);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--ink2)}
.ch.correct .ch-m{background:var(--green);border-color:var(--green);color:#fff}
.ch.wrong .ch-m{background:var(--red);border-color:var(--red);color:#fff}
.ex{display:none;background:var(--gold-l);border-radius:12px;padding:15px;margin-top:15px;font-size:13px;color:#5A3A0A;line-height:1.8}
.ex.on{display:block}.ex b{color:var(--gold)}
.qfoot{display:flex;justify-content:space-between;align-items:center;gap:12px}
.btn{font-size:14px;font-weight:700;border:none;border-radius:10px;padding:12px 24px;cursor:pointer;transition:all .15s}
.btn-p{background:var(--green);color:#fff}.btn-p:hover{background:var(--green-d)}.btn-p:disabled{background:var(--ink3);opacity:.5;cursor:not-allowed}
.btn-g{background:none;color:var(--ink2);border:1px solid var(--line)}.btn-g:hover{background:var(--line)}
.res-card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:30px;text-align:center;margin-bottom:18px}
.res-badge{font-size:58px;line-height:1;margin-bottom:8px}
.res-score{font-size:44px;font-weight:900;line-height:1}
.res-label{font-size:13px;color:var(--ink3);margin-top:8px}
.res-judge{font-size:24px;font-weight:900;margin-top:18px;padding:14px;border-radius:12px;letter-spacing:.06em}
.res-pass{background:var(--green-l);color:var(--green-d)}.res-fail{background:var(--red-l);color:var(--red)}
.res-sub{font-size:12.5px;margin-top:8px;color:var(--ink2)}
.res-k{margin-top:20px;text-align:left}
.res-kr{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid var(--line);font-size:13px}
.res-kb{flex:1;height:8px;background:var(--line);border-radius:4px;overflow:hidden}.res-kf{height:100%;border-radius:4px}
.res-act{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.note{font-size:11px;color:var(--ink3);text-align:center;margin-top:18px;line-height:1.7}
.nav{display:flex;gap:0;margin-bottom:20px;border-bottom:2px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:100;padding-top:8px}
.nav-tab{flex:1;text-align:center;padding:12px 8px;font-size:14px;font-weight:700;color:var(--ink3);cursor:pointer;border-bottom:3px solid transparent;transition:all .2s}
.nav-tab:hover{color:var(--ink)}
.nav-tab.active{color:var(--green-d);border-bottom-color:var(--green)}
.section{display:none}.section.on{display:block}
.admin-bar{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.admin-bar select,.admin-bar input{font-size:13px;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);font-family:inherit}
.admin-bar select{min-width:120px}
.admin-bar input{flex:1;min-width:180px}
.q-row{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px}
.q-row:hover{border-color:var(--green)}
.q-num{font-size:12px;font-weight:700;color:var(--ink3);min-width:30px}
.q-lv{font-size:11px;font-weight:700;color:#fff;border-radius:14px;padding:2px 10px;min-width:60px;text-align:center}
.q-cat{font-size:11px;font-weight:500;color:var(--ink3);min-width:60px}
.q-text{flex:1;font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.q-actions{display:flex;gap:6px}
.q-actions button{font-size:12px;padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:var(--card);cursor:pointer;font-family:inherit}
.q-actions button:hover{background:var(--green-l)}
.q-actions .del:hover{background:var(--red-l);border-color:var(--red)}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:1000;align-items:center;justify-content:center}
.modal-bg.on{display:flex}
.modal{background:var(--card);border-radius:18px;padding:28px;max-width:700px;width:95%;max-height:90vh;overflow-y:auto}
.modal h2{font-size:18px;font-weight:700;margin-bottom:16px;color:var(--green-d)}
.field{margin-bottom:12px}
.field label{display:block;font-size:12px;font-weight:700;color:var(--ink2);margin-bottom:4px}
.field input,.field textarea,.field select{width:100%;font-size:13px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;font-family:inherit;line-height:1.6}
.field textarea{min-height:60px;resize:vertical}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:500px){.field-row{grid-template-columns:1fr}}
.modal-foot{display:flex;gap:10px;justify-content:flex-end;margin-top:18px}
.scores-table{width:100%;border-collapse:collapse;font-size:13px}
.scores-table th{background:var(--green-d);color:#fff;padding:10px 12px;text-align:left;font-weight:500;position:sticky;top:0}
.scores-table td{padding:9px 12px;border-bottom:1px solid var(--line);background:var(--card)}
.scores-table tr:nth-child(even) td{background:#FAFBFA}
.scores-table tr:hover td{background:var(--green-l)}
.pass-badge{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px}
.pass-y{background:var(--green-l);color:var(--green-d)}
.pass-n{background:var(--red-l);color:var(--red)}
.name-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:500;align-items:center;justify-content:center}
.name-overlay.on{display:flex}
.name-box{background:var(--card);border-radius:18px;padding:30px;text-align:center;max-width:400px;width:90%}
.name-box h3{font-size:18px;margin-bottom:16px;color:var(--green-d)}
.name-box input{font-size:16px;padding:12px;border:2px solid var(--green);border-radius:10px;width:100%;text-align:center;font-family:inherit;margin-bottom:14px}
.pw-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:600;align-items:center;justify-content:center}
.pw-overlay.on{display:flex}
.pw-box{background:var(--card);border-radius:18px;padding:30px;text-align:center;max-width:400px;width:90%}
.pw-box h3{font-size:18px;margin-bottom:8px;color:var(--green-d)}
.pw-box p{font-size:12px;color:var(--ink3);margin-bottom:16px}
.pw-box input{font-size:16px;padding:12px;border:2px solid var(--green);border-radius:10px;width:100%;text-align:center;font-family:inherit;margin-bottom:14px}
.pw-err{color:var(--red);font-size:12px;margin-bottom:10px;display:none}'''

JS = r'''
const DEFAULT_DATA=%%DATA%%;
const LV=%%LV%%;
const PASS=%%PASS%%;
const KANTEN=%%KANTEN%%;

let DATA;
function loadData(){
  const s=localStorage.getItem('ict_test_data');
  if(s){try{DATA=JSON.parse(s);return;}catch(e){}}
  DATA=JSON.parse(JSON.stringify(DEFAULT_DATA));
}
function saveData(){localStorage.setItem('ict_test_data',JSON.stringify(DATA));}
function loadScores(){const s=localStorage.getItem('ict_test_scores');return s?JSON.parse(s):[];}
function saveScores(scores){localStorage.setItem('ict_test_scores',JSON.stringify(scores));}

const DEFAULT_PW='midorinkanri';
let adminUnlocked=false;
let pendingSection=null;
let pendingTab=null;

function getAdminPw(){return localStorage.getItem('ict_admin_pw')||DEFAULT_PW;}

function showSection(name,el){
  if((name==='admin'||name==='scores')&&!adminUnlocked){
    pendingSection=name;pendingTab=el;
    openPwCheck();return;
  }
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on'));
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('sec-'+name).classList.add('on');
  el.classList.add('active');
  if(name==='admin')renderAdmin();
  if(name==='scores')renderScores();
  if(name==='test'){backToSel();adminUnlocked=false;}
}
function openPwCheck(){
  document.getElementById('pwCheckOverlay').classList.add('on');
  document.getElementById('pwCheckInput').value='';
  document.getElementById('pwCheckErr').style.display='none';
  setTimeout(()=>document.getElementById('pwCheckInput').focus(),100);
}
function closePwCheck(){document.getElementById('pwCheckOverlay').classList.remove('on');pendingSection=null;pendingTab=null;}
function confirmPwCheck(){
  const input=document.getElementById('pwCheckInput').value;
  if(input===getAdminPw()){
    document.getElementById('pwCheckOverlay').classList.remove('on');
    adminUnlocked=true;
    if(pendingSection&&pendingTab)showSection(pendingSection,pendingTab);
  }else{
    document.getElementById('pwCheckErr').textContent='パスワードが違います';
    document.getElementById('pwCheckErr').style.display='block';
    document.getElementById('pwCheckInput').value='';
  }
}
function changePw(){
  document.getElementById('pwChangeOverlay').classList.add('on');
  document.getElementById('pwChangeOld').value='';
  document.getElementById('pwChangeNew1').value='';
  document.getElementById('pwChangeNew2').value='';
  document.getElementById('pwChangeErr').style.display='none';
  setTimeout(()=>document.getElementById('pwChangeOld').focus(),100);
}
function closePwChange(){document.getElementById('pwChangeOverlay').classList.remove('on');}
function confirmPwChange(){
  const old=document.getElementById('pwChangeOld').value;
  const n1=document.getElementById('pwChangeNew1').value;
  const n2=document.getElementById('pwChangeNew2').value;
  const err=document.getElementById('pwChangeErr');
  if(old!==getAdminPw()){err.textContent='現在のパスワードが違います';err.style.display='block';return;}
  if(!n1||n1.length<4){err.textContent='新しいパスワードは4文字以上にしてください';err.style.display='block';return;}
  if(n1!==n2){err.textContent='新しいパスワードが一致しません';err.style.display='block';return;}
  localStorage.setItem('ict_admin_pw',n1);
  closePwChange();
  alert('パスワードを変更しました');
}
function resetPw(){
  if(!confirm('パスワードを初期値（midorinkanri）にリセットしますか？'))return;
  localStorage.removeItem('ict_admin_pw');
  alert('パスワードを初期値にリセットしました');
}

let curLv=null,idx=0,ans=[],answered=false,sel=null,playerName='';

function grid(){
  const g=document.getElementById('grid');g.innerHTML='';
  for(let lv=1;lv<=9;lv++){
    if(!DATA[lv]||DATA[lv].length===0)continue;
    const info=LV[lv];const d=document.createElement('div');
    d.className='lv-card';d.style.setProperty('--c',info.color);d.onclick=()=>askName(lv);
    d.innerHTML=`<span class="lv-tag">${info.name}</span><div class="lv-name">${info.name}</div>
      <div class="lv-grade">${info.grade}</div><div class="lv-desc">${info.desc}</div>
      <div class="lv-foot"><span>${DATA[lv].length}問</span><span class="lv-pass">合格 ${PASS[lv]}%</span></div>`;
    g.appendChild(d);
  }
}

function askName(lv){
  curLv=lv;
  document.getElementById('nameOverlay').classList.add('on');
  document.getElementById('nameInput').value=playerName;
  setTimeout(()=>document.getElementById('nameInput').focus(),100);
}
function confirmName(){
  const n=document.getElementById('nameInput').value.trim();
  if(!n){document.getElementById('nameInput').style.borderColor='var(--red)';return;}
  playerName=n;
  document.getElementById('nameOverlay').classList.remove('on');
  startQuiz(curLv);
}
function startQuiz(lv){
  curLv=lv;idx=0;ans=[];answered=false;
  document.getElementById('sel').style.display='none';
  document.getElementById('res').classList.remove('on');
  document.getElementById('quiz').classList.add('on');
  render();scrollTo(0,0);
}
function tableHTML(t){
  let h='<table class="qtable"><thead><tr>';
  t.head.forEach(c=>h+=`<th>${c}</th>`);h+='</tr></thead><tbody>';
  t.rows.forEach(r=>{h+='<tr>';r.forEach(c=>h+=`<td>${c}</td>`);h+='</tr>';});
  return h+'</tbody></table>';
}
function render(){
  answered=false;sel=null;const qs=DATA[curLv],q=qs[idx],k=KANTEN[q.kanten];
  document.getElementById('pt').textContent=`問題 ${idx+1} / ${qs.length}`;
  document.getElementById('pf').style.width=(idx/qs.length*100)+'%';
  let body=`<span class="qk" style="background:${k.c}">${k.l}</span>`;
  if(q.link)body+=`<div class="qlink"><b>体系表との対応：</b>${q.link}</div>`;
  if(q.intro)body+=`<div class="qintro">${q.intro}</div>`;
  if(q.cond){body+='<div class="qcond">';q.cond.forEach(c=>body+=`<div>${c}</div>`);body+='</div>';}
  if(q.list){body+='<div class="qlist">';q.list.forEach(c=>body+=`<div>${c}</div>`);body+='</div>';}
  if(q.steps){body+='<div class="qsteps">';q.steps.forEach(c=>body+=`<div>${c}</div>`);body+='</div>';}
  if(q.table)body+=tableHTML(q.table);
  if(q.code)body+=`<div class="qcode">${q.code.join('\n')}</div>`;
  body+=`<div class="qt">${q.q}</div><div class="choices" id="chs"></div><div class="ex" id="ex"></div>`;
  document.getElementById('qc').innerHTML=body;
  const ch=document.getElementById('chs');
  q.choices.forEach((t,i)=>{const b=document.createElement('button');b.className='ch';
    b.innerHTML=`<span class="ch-m">${'ABCD'[i]}</span><span>${t}</span>`;b.onclick=()=>pick(i);ch.appendChild(b);});
  const btn=document.getElementById('next');btn.textContent='解答する';btn.disabled=true;btn.onclick=check;
  document.getElementById('hint').textContent='';
}
function pick(i){if(answered)return;sel=i;
  document.querySelectorAll('.ch').forEach((c,x)=>c.classList.toggle('sel',x===i));
  document.getElementById('next').disabled=false;}
function check(){if(sel===null||answered)return;answered=true;
  const q=DATA[curLv][idx],cor=q.answer;ans.push({kanten:q.kanten,correct:sel===cor});
  document.querySelectorAll('.ch').forEach((c,i)=>{c.classList.remove('sel');c.onclick=null;
    if(i===cor)c.classList.add('correct');else if(i===sel)c.classList.add('wrong');else c.classList.add('dim');});
  const ex=document.getElementById('ex');
  ex.innerHTML=`<b>${sel===cor?'正解！':'不正解'}</b><br>${q.explain}`;ex.classList.add('on');
  const btn=document.getElementById('next'),last=idx===DATA[curLv].length-1;
  btn.textContent=last?'結果をみる':'次の問題 →';btn.disabled=false;btn.onclick=nextq;
  document.getElementById('hint').textContent=sel===cor?'':`正解は ${'ABCD'[cor]}`;
}
function nextq(){if(idx<DATA[curLv].length-1){idx++;render();scrollTo(0,0);}else showResult();}
function showResult(){
  document.getElementById('quiz').classList.remove('on');
  document.getElementById('res').classList.add('on');
  const total=ans.length,cor=ans.filter(a=>a.correct).length,pct=Math.round(cor/total*100);
  const need=PASS[curLv],pass=pct>=need;
  const byK={};
  ans.forEach(a=>{if(!byK[a.kanten])byK[a.kanten]={c:0,t:0};byK[a.kanten].t++;if(a.correct)byK[a.kanten].c++;});
  let kh='';Object.keys(byK).forEach(kk=>{const k=KANTEN[kk],kp=Math.round(byK[kk].c/byK[kk].t*100);
    kh+=`<div class="res-kr"><span style="min-width:120px;font-weight:500">${k.s}</span>
      <div class="res-kb"><div class="res-kf" style="width:${kp}%;background:${k.c}"></div></div>
      <span style="min-width:70px;text-align:right">${byK[kk].c}/${byK[kk].t}（${kp}%）</span></div>`;});
  document.getElementById('rc').innerHTML=`<div class="res-badge">${pass?'🎉':'📘'}</div>
    <div class="res-score" style="color:${pass?'var(--green-d)':'var(--red)'}">${pct}<span style="font-size:22px">%</span></div>
    <div class="res-label">${LV[curLv].name}　正答 ${cor} / ${total} 問（合格基準 ${need}%）</div>
    <div class="res-judge ${pass?'res-pass':'res-fail'}">${pass?'✓ 合格':'✗ 不合格'}</div>
    <div class="res-sub">${pass?'おめでとうございます！':'合格基準にとどきませんでした。復習してもう一度挑戦しましょう。'}</div>
    <div class="res-k">${kh}</div>`;
  document.getElementById('retry').onclick=()=>startQuiz(curLv);
  const scores=loadScores();
  scores.push({name:playerName,level:curLv,correct:cor,total:total,pct:pct,pass:pass,date:new Date().toLocaleString('ja-JP')});
  saveScores(scores);
  scrollTo(0,0);
}
function backToSel(){
  document.getElementById('quiz').classList.remove('on');
  document.getElementById('res').classList.remove('on');
  document.getElementById('sel').style.display='';
  grid();
}

function stripHtml(s){if(!s)return'';const d=document.createElement('div');d.innerHTML=s;return d.textContent;}
function renderAdmin(){
  const filter=document.getElementById('adminLvFilter').value;
  const search=document.getElementById('adminSearch').value.toLowerCase();
  const list=document.getElementById('adminList');
  let html='';let count=0;
  for(let lv=1;lv<=9;lv++){
    if(filter!=='all'&&filter!==String(lv))continue;
    const qs=DATA[lv]||[];
    qs.forEach((q,i)=>{
      const text=stripHtml(q.q);
      if(search&&!text.toLowerCase().includes(search)&&!stripHtml(q.intro).toLowerCase().includes(search))return;
      const k=KANTEN[q.kanten];
      count++;
      html+=`<div class="q-row">
        <span class="q-num">${count}</span>
        <span class="q-lv" style="background:${LV[lv].color}">Lv${lv}</span>
        <span class="q-cat" style="color:${k.c}">${k.s}</span>
        <span class="q-text">${text}</span>
        <span class="q-actions">
          <button onclick="openEdit(${lv},${i})">編集</button>
          <button class="del" onclick="deleteQ(${lv},${i})">削除</button>
        </span></div>`;
    });
  }
  list.innerHTML=html||'<div style="text-align:center;padding:40px;color:var(--ink3)">問題がありません</div>';
  document.getElementById('adminCount').textContent=count+' 問を表示中';
}
let editLv=null,editIdx=null;
function openEdit(lv,i){
  if(lv===null){
    document.getElementById('editTitle').textContent='問題を追加';
    editLv=null;editIdx=null;
    ['edLv','edKanten','edLink','edIntro','edQ','edA','edB','edC','edD','edAns','edExplain'].forEach(id=>{
      const el=document.getElementById(id);if(el.tagName==='SELECT')el.selectedIndex=0;else el.value='';});
  }else{
    document.getElementById('editTitle').textContent='問題を編集';
    editLv=lv;editIdx=i;
    const q=DATA[lv][i];
    document.getElementById('edLv').value=lv;
    document.getElementById('edKanten').value=q.kanten;
    document.getElementById('edLink').value=q.link||'';
    document.getElementById('edIntro').value=q.intro||'';
    document.getElementById('edQ').value=q.q||'';
    document.getElementById('edA').value=q.choices[0]||'';
    document.getElementById('edB').value=q.choices[1]||'';
    document.getElementById('edC').value=q.choices[2]||'';
    document.getElementById('edD').value=q.choices[3]||'';
    document.getElementById('edAns').value=q.answer;
    document.getElementById('edExplain').value=q.explain||'';
  }
  document.getElementById('editModal').classList.add('on');
}
function closeEdit(){document.getElementById('editModal').classList.remove('on');}
function saveEdit(){
  const q={
    kanten:document.getElementById('edKanten').value,
    link:document.getElementById('edLink').value,
    intro:document.getElementById('edIntro').value,
    q:document.getElementById('edQ').value,
    choices:[document.getElementById('edA').value,document.getElementById('edB').value,
             document.getElementById('edC').value,document.getElementById('edD').value],
    answer:parseInt(document.getElementById('edAns').value),
    explain:document.getElementById('edExplain').value
  };
  if(!q.q){alert('問題文を入力してください');return;}
  const targetLv=document.getElementById('edLv').value;
  if(editLv!==null){
    if(String(editLv)===targetLv){DATA[editLv][editIdx]=q;}
    else{DATA[editLv].splice(editIdx,1);if(!DATA[targetLv])DATA[targetLv]=[];DATA[targetLv].push(q);}
  }else{
    if(!DATA[targetLv])DATA[targetLv]=[];DATA[targetLv].push(q);
  }
  saveData();closeEdit();renderAdmin();
}
function deleteQ(lv,i){
  if(!confirm('この問題を削除しますか？'))return;
  DATA[lv].splice(i,1);saveData();renderAdmin();
}
function exportData(){
  const blob=new Blob([JSON.stringify(DATA,null,2)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='ICT_test_data.json';a.click();
}
function importData(e){
  const file=e.target.files[0];if(!file)return;
  const r=new FileReader();
  r.onload=function(){
    try{
      const d=JSON.parse(r.result);
      if(confirm('現在のデータを上書きしますか？')){DATA=d;saveData();renderAdmin();alert('インポート完了');}
    }catch(er){alert('JSONファイルの形式が正しくありません');}
  };
  r.readAsText(file);e.target.value='';
}
function resetData(){
  if(!confirm('問題データを初期状態に戻しますか？追加・編集した内容はすべて失われます。'))return;
  DATA=JSON.parse(JSON.stringify(DEFAULT_DATA));
  saveData();renderAdmin();alert('初期状態に戻しました');
}

function renderScores(){
  const filter=document.getElementById('scoreLvFilter').value;
  const search=document.getElementById('scoreSearch').value.toLowerCase();
  const scores=loadScores();
  const body=document.getElementById('scoreBody');
  let html='';let count=0;
  scores.slice().reverse().forEach((s,ri)=>{
    const i=scores.length-1-ri;
    if(filter!=='all'&&String(s.level)!==filter)return;
    if(search&&!s.name.toLowerCase().includes(search))return;
    html+=`<tr>
      <td>${s.name}</td>
      <td>レベル${s.level}</td>
      <td>${s.correct} / ${s.total}</td>
      <td>${s.pct}%</td>
      <td><span class="pass-badge ${s.pass?'pass-y':'pass-n'}">${s.pass?'合格':'不合格'}</span></td>
      <td>${s.date}</td>
      <td><button onclick="deleteScore(${i})" style="font-size:11px;padding:3px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);cursor:pointer">削除</button></td>
    </tr>`;
    count++;
  });
  body.innerHTML=html||'<tr><td colspan="7" style="text-align:center;padding:30px;color:var(--ink3)">成績データがありません</td></tr>';
  document.getElementById('scoreCount').textContent=count+' 件の記録';
}
function deleteScore(i){
  if(!confirm('この記録を削除しますか？'))return;
  const scores=loadScores();scores.splice(i,1);saveScores(scores);renderScores();
}
function clearScores(){
  if(!confirm('全成績データを削除しますか？この操作は取り消せません。'))return;
  saveScores([]);renderScores();
}
function exportScoresCSV(){
  const scores=loadScores();
  if(!scores.length){alert('データがありません');return;}
  let csv='﻿名前,レベル,正答数,問題数,正答率(%),合否,受験日時\n';
  scores.forEach(s=>{
    csv+=`${s.name},レベル${s.level},${s.correct},${s.total},${s.pct},${s.pass?'合格':'不合格'},${s.date}\n`;
  });
  const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='ICT_test_scores.csv';a.click();
}

loadData();grid();
'''

BODY = '''<div class="app">
<div class="hd"><h1>みどりの学園 ICT活用能力認定テスト</h1>
<p>文部科学省「情報活用能力調査」習熟度レベル準拠 / 全9レベル / 管理版</p></div>

<div class="nav">
<div class="nav-tab active" onclick="showSection('test',this)">テスト受験</div>
<div class="nav-tab" onclick="showSection('admin',this)">問題管理</div>
<div class="nav-tab" onclick="showSection('scores',this)">成績一覧</div>
</div>

<div class="section on" id="sec-test">
<div id="sel">
<div class="banner"><b>このテストの特ちょう：</b>文部科学省の改訂方向性（2026年5月）にもとづき、AIに指示して課題を解決する時代の「<b>プログラミング的思考</b>」と、生成AIのファクトチェックを重視しています。</div>
<div class="intro">各レベル20問・4観点（操作／情報活用／プログラミング／情報モラル）で構成。挑戦するレベルを選んでください。
<div class="src">出典：文部科学省「情報活用能力調査（令和3年度）」結果等を参考に作成</div></div>
<div class="lv-grid" id="grid"></div></div>
<div class="quiz" id="quiz">
<div class="qbar"><button class="qback" onclick="backToSel()">&#8592; レベル選択</button>
<div class="qprog"><div class="qprog-t" id="pt">問題 1 / 20</div><div class="qprog-b"><div class="qprog-f" id="pf"></div></div></div></div>
<div class="qcard" id="qc"></div>
<div class="qfoot"><span id="hint" style="font-size:12px;color:var(--ink3)"></span><button class="btn btn-p" id="next" disabled>解答する</button></div></div>
<div class="result" id="res"><div class="res-card" id="rc"></div>
<div class="res-act"><button class="btn btn-g" onclick="backToSel()">レベル選択にもどる</button><button class="btn btn-p" id="retry">もう一度挑戦</button></div>
<div class="note">※ このテストは習熟度レベルの目安を確認するものです。</div></div>
</div>

<div class="section" id="sec-admin">
<div class="admin-bar">
<select id="adminLvFilter" onchange="renderAdmin()">
<option value="all">全レベル</option>
<option value="1">レベル1</option><option value="2">レベル2</option><option value="3">レベル3</option>
<option value="4">レベル4</option><option value="5">レベル5</option><option value="6">レベル6</option>
<option value="7">レベル7</option><option value="8">レベル8</option><option value="9">レベル9</option>
</select>
<input type="text" id="adminSearch" placeholder="問題を検索..." oninput="renderAdmin()">
<button class="btn btn-p" onclick="openEdit(null)" style="padding:8px 16px;font-size:13px">+ 問題を追加</button>
<button class="btn btn-g" onclick="exportData()" style="padding:8px 16px;font-size:13px">エクスポート</button>
<button class="btn btn-g" onclick="document.getElementById('importFile').click()" style="padding:8px 16px;font-size:13px">インポート</button>
<button class="btn btn-g" onclick="changePw()" style="padding:8px 16px;font-size:13px">PW変更</button>
<button class="btn btn-g" onclick="resetPw()" style="padding:8px 16px;font-size:13px">PWリセット</button>
<button class="btn btn-g" onclick="resetData()" style="padding:8px 16px;font-size:13px;color:var(--red)">問題初期化</button>
<input type="file" id="importFile" accept=".json" style="display:none" onchange="importData(event)">
</div>
<div id="adminList"></div>
<div style="text-align:center;margin-top:14px;font-size:12px;color:var(--ink3)" id="adminCount"></div>
</div>

<div class="section" id="sec-scores">
<div class="admin-bar">
<select id="scoreLvFilter" onchange="renderScores()">
<option value="all">全レベル</option>
<option value="1">レベル1</option><option value="2">レベル2</option><option value="3">レベル3</option>
<option value="4">レベル4</option><option value="5">レベル5</option><option value="6">レベル6</option>
<option value="7">レベル7</option><option value="8">レベル8</option><option value="9">レベル9</option>
</select>
<input type="text" id="scoreSearch" placeholder="名前を検索..." oninput="renderScores()">
<button class="btn btn-g" onclick="exportScoresCSV()" style="padding:8px 16px;font-size:13px">CSV出力</button>
<button class="btn btn-g" onclick="clearScores()" style="padding:8px 16px;font-size:13px;color:var(--red)">全削除</button>
</div>
<div style="overflow-x:auto">
<table class="scores-table">
<thead><tr><th>名前</th><th>レベル</th><th>得点</th><th>正答率</th><th>合否</th><th>受験日時</th><th>操作</th></tr></thead>
<tbody id="scoreBody"></tbody>
</table>
</div>
<div style="text-align:center;margin-top:14px;font-size:12px;color:var(--ink3)" id="scoreCount"></div>
</div>
</div>

<div class="name-overlay" id="nameOverlay">
<div class="name-box">
<h3>名前を入力してください</h3>
<input type="text" id="nameInput" placeholder="例：田中太郎" onkeydown="if(event.key==='Enter')confirmName()">
<br><button class="btn btn-p" onclick="confirmName()" style="width:100%">テストを開始する</button>
</div>
</div>

<div class="pw-overlay" id="pwCheckOverlay">
<div class="pw-box">
<h3>管理パスワード</h3>
<p>問題管理・成績一覧を表示するにはパスワードを入力してください</p>
<input type="password" id="pwCheckInput" placeholder="パスワード" onkeydown="if(event.key==='Enter')confirmPwCheck()">
<div class="pw-err" id="pwCheckErr"></div>
<button class="btn btn-p" onclick="confirmPwCheck()" style="width:100%">ログイン</button>
<br><button class="btn btn-g" onclick="closePwCheck()" style="width:100%;margin-top:8px">キャンセル</button>
</div>
</div>

<div class="pw-overlay" id="pwChangeOverlay">
<div class="pw-box">
<h3>パスワード変更</h3>
<p>管理パスワードを変更します</p>
<input type="password" id="pwChangeOld" placeholder="現在のパスワード" onkeydown="if(event.key==='Enter')document.getElementById('pwChangeNew1').focus()">
<input type="password" id="pwChangeNew1" placeholder="新しいパスワード（4文字以上）" onkeydown="if(event.key==='Enter')document.getElementById('pwChangeNew2').focus()">
<input type="password" id="pwChangeNew2" placeholder="新しいパスワード（確認）" onkeydown="if(event.key==='Enter')confirmPwChange()">
<div class="pw-err" id="pwChangeErr"></div>
<button class="btn btn-p" onclick="confirmPwChange()" style="width:100%">変更する</button>
<br><button class="btn btn-g" onclick="closePwChange()" style="width:100%;margin-top:8px">キャンセル</button>
</div>
</div>

<div class="modal-bg" id="editModal">
<div class="modal">
<h2 id="editTitle">問題を編集</h2>
<div class="field-row">
<div class="field"><label>レベル</label><select id="edLv"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select></div>
<div class="field"><label>観点</label><select id="edKanten"><option value="op">操作</option><option value="info">情報活用</option><option value="prog">プログラミング</option><option value="moral">情報モラル</option></select></div>
</div>
<div class="field"><label>体系表との対応（link）</label><input id="edLink"></div>
<div class="field"><label>導入文（intro）</label><textarea id="edIntro"></textarea></div>
<div class="field"><label>問題文</label><textarea id="edQ" style="min-height:80px"></textarea></div>
<div class="field"><label>選択肢A</label><input id="edA"></div>
<div class="field"><label>選択肢B</label><input id="edB"></div>
<div class="field"><label>選択肢C</label><input id="edC"></div>
<div class="field"><label>選択肢D</label><input id="edD"></div>
<div class="field-row">
<div class="field"><label>正解</label><select id="edAns"><option value="0">A</option><option value="1">B</option><option value="2">C</option><option value="3">D</option></select></div>
<div class="field"></div>
</div>
<div class="field"><label>解説</label><textarea id="edExplain"></textarea></div>
<div class="modal-foot">
<button class="btn btn-g" onclick="closeEdit()">キャンセル</button>
<button class="btn btn-p" onclick="saveEdit()">保存</button>
</div>
</div>
</div>'''

# Replace placeholders in JS
js_final = JS.replace('%%DATA%%', data_js).replace('%%LV%%', lv_js).replace('%%PASS%%', pass_js).replace('%%KANTEN%%', kanten_js)

html = f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>みどりの学園 ICT活用能力認定テスト（管理版）</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{BODY}
<script>{js_final}</script></body></html>'''

out = Path(r'C:\Users\natuk\Desktop\みどりの学園\ICT認定テスト_管理版.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Created: {out.name}")
print(f"Size: {out.stat().st_size / 1024:.1f} KB")
