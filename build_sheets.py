import re, json
from pathlib import Path

html_file = Path(r'C:\Users\natuk\Downloads\ICT認定テスト_改訂版_全レベル_2.html')
with open(html_file, 'r', encoding='utf-8') as f:
    original = f.read()

data_js = re.search(r'const\s+DATA\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
lv_js = re.search(r'const\s+LV\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
pass_js = re.search(r'const\s+PASS\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)
kanten_js = re.search(r'const\s+KANTEN\s*=\s*(\{.+?\});', original, re.DOTALL).group(1)

questions_sheet_id = "1ao_won5Vwks_4sRaE1h-imoh-4e5uX8dp0O1lIN6-W0"
scores_sheet_id = "1PpbgF776svxwVmKqz3rlRhb25cnjxMXvAil4sghUfGk"

# Read existing HTML structure
with open(Path(r'C:\Users\natuk\Desktop\みどりの学園\ICT認定テスト_管理版.html'), 'r', encoding='utf-8') as f:
    existing = f.read()

# Extract CSS
css_match = re.search(r'<style>(.*?)</style>', existing, re.DOTALL)
css = css_match.group(1) if css_match else ""

# Extract BODY (simplified for sheets version)
body = '''<div class="app">
<div class="hd"><h1>みどりの学園 ICT活用能力認定テスト</h1>
<p>文部科学省「情報活用能力調査」習熟度レベル準拠 / Web版</p></div>

<div class="nav">
<div class="nav-tab active" onclick="showSection('test',this)">テスト受験</div>
<div class="nav-tab" onclick="showSection('admin',this)">問題管理</div>
<div class="nav-tab" onclick="showSection('scores',this)">成績一覧</div>
</div>

<div class="section on" id="sec-test">
<div id="sel">
<div class="banner"><b>このテストの特ちょう：</b>文部科学省の改訂方向性（2026年5月）にもとづき、AIに指示して課題を解決する時代の「プログラミング的思考」と、生成AIのファクトチェックを重視しています。</div>
<div class="intro">各レベル20問・4観点（操作／情報活用／プログラミング／情報モラル）で構成。挑戦するレベルを選んでください。
<div class="src">出典：文部科学省「情報活用能力調査（令和3年度）」結果等を参考に作成</div></div>
<div class="lv-grid" id="grid"></div></div>
<div class="quiz" id="quiz">
<div class="qbar"><button class="qback" onclick="backToSel()">← レベル選択</button>
<div class="qprog"><div class="qprog-t" id="pt">問題 1 / 20</div><div class="qprog-b"><div class="qprog-f" id="pf"></div></div></div></div>
<div class="qcard" id="qc"></div>
<div class="qfoot"><span id="hint" style="font-size:12px;color:var(--ink3)"></span><button class="btn btn-p" id="next" disabled>解答する</button></div></div>
<div class="result" id="res"><div class="res-card" id="rc"></div>
<div class="res-act"><button class="btn btn-g" onclick="backToSel()">レベル選択にもどる</button><button class="btn btn-p" id="retry">もう一度挑戦</button></div>
<div class="note">※ テスト受験後、成績は自動的にGoogle Sheetsに保存されます。</div></div>
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
<button class="btn btn-g" onclick="changePw()" style="padding:8px 16px;font-size:13px">PW変更</button>
<button class="btn btn-g" onclick="resetPw()" style="padding:8px 16px;font-size:13px">PWリセット</button>
</div>
<div id="adminList"></div>
<div style="text-align:center;margin-top:14px;font-size:12px;color:var(--ink3)" id="adminCount"></div>
</div>

<div class="section" id="sec-scores">
<div style="text-align:center;padding:40px;color:var(--ink3)"><p>成績はGoogle Sheetsに自動記録されます。</p><p style="margin-top:10px;"><a href="https://docs.google.com/spreadsheets/d/1PpbgF776svxwVmKqz3rlRhb25cnjxMXvAil4sghUfGk" target="_blank" class="btn btn-p" style="display:inline-block">成績シートを開く</a></p></div>
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
<div class="field"><label>条件（cond・JSON形式）</label><textarea id="edCond" placeholder='["条件1","条件2"]'></textarea></div>
<div class="field"><label>リスト（list・JSON形式）</label><textarea id="edList" placeholder='["項目1","項目2","項目3"]'></textarea></div>
<div class="field"><label>テーブル（table・JSON形式）</label><textarea id="edTable" placeholder='{"head":["列1","列2"],"rows":[["値1","値2"]]}'></textarea></div>
<div class="field"><label>コード（code）</label><textarea id="edCode" placeholder='コードブロック'></textarea></div>
<div class="field"><label>ステップ（steps・JSON形式）</label><textarea id="edSteps" placeholder='["ステップ1","ステップ2"]'></textarea></div>
<div class="field"><label>問題文</label><textarea id="edQ" style="min-height:80px"></textarea></div>
<div class="field"><label>選択肢A</label><input id="edA"></div>
<div class="field"><label>選択肢B</label><input id="edB"></div>
<div class="field"><label>選択肢C</label><input id="edC"></div>
<div class="field"><label>選択肢D</label><input id="edD"></div>
<div class="field-row">
<div class="field"><label>正解</label><select id="edAns"><option value="0">A</option><option value="1">B</option><option value="2">C</option><option value="3">D</option></select></div>
<div class="field"><label>解説</label><textarea id="edExplain" style="min-height:60px"></textarea></div>
</div>
<div class="modal-foot">
<button class="btn btn-g" onclick="closeEdit()">キャンセル</button>
<button class="btn btn-p" onclick="saveEdit()">保存する</button>
</div>
</div>
</div>
</div>'''

js = f'''
const DEFAULT_DATA={data_js};
const LV={lv_js};
const PASS={pass_js};
const KANTEN={kanten_js};
const QUESTIONS_SHEET_ID="{questions_sheet_id}";
const SCORES_SHEET_ID="{scores_sheet_id}";

let DATA;
let adminUnlocked=false;
let pendingSection=null;
let pendingTab=null;
const DEFAULT_PW='midorinkanri';

function getAdminPw(){{return localStorage.getItem('ict_admin_pw')||DEFAULT_PW;}}

function loadData(){{DATA=JSON.parse(JSON.stringify(DEFAULT_DATA));}}

function showSection(name,el){{
  if((name==='admin'||name==='scores')&&!adminUnlocked){{
    pendingSection=name;pendingTab=el;
    openPwCheck();return;
  }}
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('on'));
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('sec-'+name).classList.add('on');
  el.classList.add('active');
  if(name==='test'){{backToSel();adminUnlocked=false;}}
}}

function openPwCheck(){{
  document.getElementById('pwCheckOverlay').classList.add('on');
  document.getElementById('pwCheckInput').value='';
  document.getElementById('pwCheckErr').style.display='none';
  setTimeout(()=>document.getElementById('pwCheckInput').focus(),100);
}}

function closePwCheck(){{document.getElementById('pwCheckOverlay').classList.remove('on');pendingSection=null;pendingTab=null;}}

function confirmPwCheck(){{
  const input=document.getElementById('pwCheckInput').value;
  if(input===getAdminPw()){{
    document.getElementById('pwCheckOverlay').classList.remove('on');
    adminUnlocked=true;
    if(pendingSection&&pendingTab)showSection(pendingSection,pendingTab);
  }}else{{
    document.getElementById('pwCheckErr').textContent='パスワードが違います';
    document.getElementById('pwCheckErr').style.display='block';
    document.getElementById('pwCheckInput').value='';
  }}
}}

function changePw(){{
  document.getElementById('pwChangeOverlay').classList.add('on');
  document.getElementById('pwChangeOld').value='';
  document.getElementById('pwChangeNew1').value='';
  document.getElementById('pwChangeNew2').value='';
  document.getElementById('pwChangeErr').style.display='none';
  setTimeout(()=>document.getElementById('pwChangeOld').focus(),100);
}}

function closePwChange(){{document.getElementById('pwChangeOverlay').classList.remove('on');}}

function confirmPwChange(){{
  const old=document.getElementById('pwChangeOld').value;
  const n1=document.getElementById('pwChangeNew1').value;
  const n2=document.getElementById('pwChangeNew2').value;
  const err=document.getElementById('pwChangeErr');
  if(old!==getAdminPw()){{err.textContent='現在のパスワードが違います';err.style.display='block';return;}}
  if(!n1||n1.length<4){{err.textContent='新しいパスワードは4文字以上にしてください';err.style.display='block';return;}}
  if(n1!==n2){{err.textContent='新しいパスワードが一致しません';err.style.display='block';return;}}
  localStorage.setItem('ict_admin_pw',n1);
  closePwChange();
  alert('パスワードを変更しました');
}}

function resetPw(){{
  if(!confirm('パスワードを初期値（midorinkanri）にリセットしますか？'))return;
  localStorage.removeItem('ict_admin_pw');
  alert('パスワードを初期値にリセットしました');
}}

let curLv=null,idx=0,ans=[],answered=false,sel=null,playerName='';

function grid(){{
  const g=document.getElementById('grid');g.innerHTML='';
  for(let lv=1;lv<=9;lv++){{
    if(!DATA[lv]||DATA[lv].length===0)continue;
    const info=LV[lv];const d=document.createElement('div');
    d.className='lv-card';d.style.setProperty('--c',info.color);d.onclick=()=>askName(lv);
    d.innerHTML=`<span class="lv-tag">${{info.name}}</span><div class="lv-name">${{info.name}}</div>
      <div class="lv-grade">${{info.grade}}</div><div class="lv-desc">${{info.desc}}</div>
      <div class="lv-foot"><span>${{DATA[lv].length}}問</span><span class="lv-pass">合格 ${{PASS[lv]}}%</span></div>`;
    g.appendChild(d);
  }}
}}

function askName(lv){{
  curLv=lv;
  document.getElementById('nameOverlay').classList.add('on');
  document.getElementById('nameInput').value=playerName;
  setTimeout(()=>document.getElementById('nameInput').focus(),100);
}}

function confirmName(){{
  const n=document.getElementById('nameInput').value.trim();
  if(!n){{document.getElementById('nameInput').style.borderColor='var(--red)';return;}}
  playerName=n;
  document.getElementById('nameOverlay').classList.remove('on');
  startQuiz(curLv);
}}

function startQuiz(lv){{
  curLv=lv;idx=0;ans=[];answered=false;
  document.getElementById('sel').style.display='none';
  document.getElementById('res').classList.remove('on');
  document.getElementById('quiz').classList.add('on');
  render();scrollTo(0,0);
}}

function render(){{
  answered=false;sel=null;const qs=DATA[curLv],q=qs[idx],k=KANTEN[q.kanten];
  document.getElementById('pt').textContent=`問題 ${{idx+1}} / ${{qs.length}}`;
  document.getElementById('pf').style.width=(idx/qs.length*100)+'%';
  let body=`<span class="qk" style="background:${{k.c}}">${{k.l}}</span>`;
  if(q.link)body+=`<div class="qlink"><b>体系表との対応：</b>${{q.link}}</div>`;
  if(q.intro)body+=`<div class="qintro">${{q.intro}}</div>`;
  if(q.cond){{if(Array.isArray(q.cond)){{let condHtml='<div class="qcond">';q.cond.forEach(c=>{{condHtml+=`<div>${{c}}</div>`;}});condHtml+='</div>';body+=condHtml;}}else{{body+=`<div class="qcond"><div>${{q.cond}}</div></div>`;}}}}
  if(q.list){{let listHtml='<div class="qlist">';q.list.forEach(item=>{{listHtml+=`<div>${{item}}</div>`;}});listHtml+='</div>';body+=listHtml;}}
  if(q.table){{let tblHtml='<table class="qtable"><thead><tr>';q.table.head.forEach(h=>{{tblHtml+=`<th>${{h}}</th>`;}});tblHtml+='</tr></thead><tbody>';q.table.rows.forEach(row=>{{tblHtml+='<tr>';row.forEach(cell=>{{tblHtml+=`<td>${{cell}}</td>`;}});tblHtml+='</tr>';}});tblHtml+='</tbody></table>';body+=tblHtml;}}
  if(q.code)body+=`<div class="qcode">${{q.code}}</div>`;
  if(q.steps){{if(Array.isArray(q.steps)){{let stepsHtml='<div class="qsteps">';q.steps.forEach(s=>{{stepsHtml+=`<div>${{s}}</div>`;}});stepsHtml+='</div>';body+=stepsHtml;}}else{{body+=`<div class="qsteps"><div>${{q.steps}}</div></div>`;}}}}
  body+=`<div class="qt">${{q.q}}</div><div class="choices" id="chs"></div><div class="ex" id="ex"></div>`;
  document.getElementById('qc').innerHTML=body;
  const ch=document.getElementById('chs');
  q.choices.forEach((t,i)=>{{const b=document.createElement('button');b.className='ch';
    b.innerHTML=`<span class="ch-m">${{'ABCD'[i]}}</span><span>${{t}}</span>`;b.onclick=()=>pick(i);ch.appendChild(b);}});
  const btn=document.getElementById('next');btn.textContent='解答する';btn.disabled=true;btn.onclick=check;
  document.getElementById('hint').textContent='';
}}

function pick(i){{if(answered)return;sel=i;
  document.querySelectorAll('.ch').forEach((c,x)=>c.classList.toggle('sel',x===i));
  document.getElementById('next').disabled=false;}}

function check(){{if(sel===null||answered)return;answered=true;
  const q=DATA[curLv][idx],cor=q.answer;ans.push({{kanten:q.kanten,correct:sel===cor}});
  document.querySelectorAll('.ch').forEach((c,i)=>{{c.classList.remove('sel');c.onclick=null;
    if(i===cor)c.classList.add('correct');else if(i===sel)c.classList.add('wrong');else c.classList.add('dim');}});
  const ex=document.getElementById('ex');
  ex.innerHTML=`<b>${{sel===cor?'正解！':'不正解'}}</b><br>${{q.explain}}`;ex.classList.add('on');
  const btn=document.getElementById('next'),last=idx===DATA[curLv].length-1;
  btn.textContent=last?'結果をみる':'次の問題 →';btn.disabled=false;btn.onclick=nextq;
  document.getElementById('hint').textContent=sel===cor?'':`正解は ${{['A','B','C','D'][cor]}}`;
}}

function nextq(){{if(idx<DATA[curLv].length-1){{idx++;render();scrollTo(0,0);}}else showResult();}}

function showResult(){{
  document.getElementById('quiz').classList.remove('on');
  document.getElementById('res').classList.add('on');
  const total=ans.length,cor=ans.filter(a=>a.correct).length,pct=Math.round(cor/total*100);
  const need=PASS[curLv],pass=pct>=need;
  const byK={{}};
  ans.forEach(a=>{{if(!byK[a.kanten])byK[a.kanten]={{c:0,t:0}};byK[a.kanten].t++;if(a.correct)byK[a.kanten].c++;}});
  let kh='';Object.keys(byK).forEach(kk=>{{const k=KANTEN[kk],kp=Math.round(byK[kk].c/byK[kk].t*100);
    kh+=`<div class="res-kr"><span style="min-width:120px;font-weight:500">${{k.s}}</span>
      <div class="res-kb"><div class="res-kf" style="width:${{kp}}%;background:${{k.c}}"></div></div>
      <span style="min-width:70px;text-align:right">${{byK[kk].c}}/${{byK[kk].t}}（${{kp}}%）</span></div>`;}});
  document.getElementById('rc').innerHTML=`<div class="res-badge">${{pass?'🎉':'📘'}}</div>
    <div class="res-score" style="color:${{pass?'var(--green-d)':'var(--red)'}}">${{pct}}<span style="font-size:22px">%</span></div>
    <div class="res-label">${{LV[curLv].name}}　正答 ${{cor}} / ${{total}} 問（合格基準 ${{need}}%）</div>
    <div class="res-judge ${{pass?'res-pass':'res-fail'}}">${{pass?'✓ 合格':'✗ 不合格'}}</div>
    <div class="res-sub">${{pass?'おめでとうございます！':'合格基準にとどきませんでした。復習してもう一度挑戦しましょう。'}}</div>
    <div class="res-k">${{kh}}</div>`;
  document.getElementById('retry').onclick=()=>startQuiz(curLv);
  const date=new Date().toLocaleString('ja-JP');
  saveScoreToSheets(playerName,curLv,cor,total,pct,pass,date);
  scrollTo(0,0);
}}

function saveScoreToSheets(name,level,correct,total,pct,pass,date){{
  const url=`https://docs.google.com/forms/d/e/1FAIpQLSc_placeholder/formResponse`;
  const data=new FormData();
  data.append('entry.0',name);
  data.append('entry.1',level);
  data.append('entry.2',correct);
  data.append('entry.3',total);
  data.append('entry.4',pct);
  data.append('entry.5',pass?'合格':'不合格');
  data.append('entry.6',date);
  fetch(url,{{method:'POST',body:data,mode:'no-cors'}}).catch(e=>console.log('Score saved (offline ok)',e));
}}

function backToSel(){{
  document.getElementById('quiz').classList.remove('on');
  document.getElementById('res').classList.remove('on');
  document.getElementById('sel').style.display='';
  grid();
}}

function stripHtml(s){{if(!s)return'';const d=document.createElement('div');d.innerHTML=s;return d.textContent;}}
function renderAdmin(){{
  const filter=document.getElementById('adminLvFilter').value;
  const search=document.getElementById('adminSearch').value.toLowerCase();
  const list=document.getElementById('adminList');
  let html='';let count=0;
  for(let lv=1;lv<=9;lv++){{
    if(filter!=='all'&&filter!==String(lv))continue;
    const qs=DATA[lv]||[];
    qs.forEach((q,i)=>{{
      const text=stripHtml(q.q);
      if(search&&!text.toLowerCase().includes(search)&&!stripHtml(q.intro).toLowerCase().includes(search))return;
      const k=KANTEN[q.kanten];
      count++;
      html+=`<div class="q-row">
        <span class="q-num">${{count}}</span>
        <span class="q-lv" style="background:${{LV[lv].color}}">Lv${{lv}}</span>
        <span class="q-cat">${{k.s}}</span>
        <span class="q-text">${{stripHtml(q.q)}}</span>
        <div class="q-actions">
          <button onclick="openEdit(${{lv}},${{i}})">編集</button>
          <button class="del" onclick="deleteQ(${{lv}},${{i}})">削除</button>
        </div>
      </div>`;
    }});
  }}
  list.innerHTML=html||'<div style="text-align:center;padding:40px;color:var(--ink3)">問題がありません</div>';
  document.getElementById('adminCount').textContent=count+' 問を表示中';
}}
let editLv=null,editIdx=null;
function openEdit(lv,i){{
  if(lv===null){{
    document.getElementById('editTitle').textContent='問題を追加';
    editLv=null;editIdx=null;
    ['edLv','edKanten','edLink','edIntro','edCond','edList','edTable','edCode','edSteps','edQ','edA','edB','edC','edD','edAns','edExplain'].forEach(id=>{{
      const el=document.getElementById(id);if(el.tagName==='SELECT')el.selectedIndex=0;else el.value='';}});
  }}else{{
    document.getElementById('editTitle').textContent='問題を編集';
    editLv=lv;editIdx=i;
    const q=DATA[lv][i];
    document.getElementById('edLv').value=lv;
    document.getElementById('edKanten').value=q.kanten;
    document.getElementById('edLink').value=q.link||'';
    document.getElementById('edIntro').value=q.intro||'';
    document.getElementById('edCond').value=q.cond?JSON.stringify(q.cond):'';
    document.getElementById('edList').value=q.list?JSON.stringify(q.list):'';
    document.getElementById('edTable').value=q.table?JSON.stringify(q.table):'';
    document.getElementById('edCode').value=q.code||'';
    document.getElementById('edSteps').value=q.steps?JSON.stringify(q.steps):'';
    document.getElementById('edQ').value=q.q||'';
    document.getElementById('edA').value=q.choices[0]||'';
    document.getElementById('edB').value=q.choices[1]||'';
    document.getElementById('edC').value=q.choices[2]||'';
    document.getElementById('edD').value=q.choices[3]||'';
    document.getElementById('edAns').value=q.answer;
    document.getElementById('edExplain').value=q.explain||'';
  }}
  document.getElementById('editModal').classList.add('on');
}}
function closeEdit(){{document.getElementById('editModal').classList.remove('on');}}
function saveEdit(){{
  const q={{
    kanten:document.getElementById('edKanten').value,
    link:document.getElementById('edLink').value||undefined,
    intro:document.getElementById('edIntro').value||undefined,
    q:document.getElementById('edQ').value,
    choices:[document.getElementById('edA').value,document.getElementById('edB').value,
             document.getElementById('edC').value,document.getElementById('edD').value],
    answer:parseInt(document.getElementById('edAns').value),
    explain:document.getElementById('edExplain').value||undefined
  }};
  const condStr=document.getElementById('edCond').value.trim();
  if(condStr){{try{{q.cond=JSON.parse(condStr);}}catch(e){{alert('条件のJSON形式が不正です');return;}}}}
  const listStr=document.getElementById('edList').value.trim();
  if(listStr){{try{{q.list=JSON.parse(listStr);}}catch(e){{alert('リストのJSON形式が不正です');return;}}}}
  const tableStr=document.getElementById('edTable').value.trim();
  if(tableStr){{try{{q.table=JSON.parse(tableStr);}}catch(e){{alert('テーブルのJSON形式が不正です');return;}}}}
  const codeStr=document.getElementById('edCode').value.trim();
  if(codeStr)q.code=codeStr;
  const stepsStr=document.getElementById('edSteps').value.trim();
  if(stepsStr){{try{{q.steps=JSON.parse(stepsStr);}}catch(e){{alert('ステップのJSON形式が不正です');return;}}}}
  if(!q.q){{alert('問題文を入力してください');return;}}
  const targetLv=document.getElementById('edLv').value;
  if(editLv!==null){{
    if(String(editLv)===targetLv){{DATA[editLv][editIdx]=q;}}
    else{{DATA[editLv].splice(editIdx,1);if(!DATA[targetLv])DATA[targetLv]=[];DATA[targetLv].push(q);}}
  }}else{{
    if(!DATA[targetLv])DATA[targetLv]=[];DATA[targetLv].push(q);
  }}
  closeEdit();renderAdmin();
}}
function deleteQ(lv,i){{
  if(!confirm('この問題を削除しますか？'))return;
  DATA[lv].splice(i,1);renderAdmin();
}}

loadData();
grid();
renderAdmin();
'''

html = f'''<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>みどりの学園 ICT活用能力認定テスト</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{body}
<script>{js}</script></body></html>'''

out = Path(r'C:\Users\natuk\Desktop\みどりの学園\ICT認定テスト_Web版.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Created: {out.name}")
print(f"Size: {out.stat().st_size / 1024:.1f} KB")
print("\nSheets Info:")
print(f"Questions: https://docs.google.com/spreadsheets/d/{questions_sheet_id}")
print(f"Scores: https://docs.google.com/spreadsheets/d/{scores_sheet_id}")
