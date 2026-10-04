/* One Word and One Word Advanced. The page never holds the day's word: each guess is scored by The Well's server,
   which reveals the word and its teaching only when the game ends. Your game is saved in this browser for the day. */
(function(){
"use strict";
var API="https://well-board.dustin-nimmo.workers.dev";
var ADV=window.OW_ED==="advanced",ED=ADV?"advanced":"regular",L=ADV?7:5,TR=ADV?7:6;
var NUMW=["zero","one","two","three","four","five","six","seven"];
function cap(s){return s.charAt(0).toUpperCase()+s.slice(1)}

/* ---------- day + storage ---------- */
var now=new Date();
var dayIdx=Math.round((Date.UTC(now.getFullYear(),now.getMonth(),now.getDate())-Date.UTC(2026,9,2))/864e5);
var no=Math.max(1,dayIdx+1);
var DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],MON=["January","February","March","April","May","June","July","August","September","October","November","December"];
document.getElementById("date").textContent=DAYS[now.getDay()]+" · "+MON[now.getMonth()]+" "+now.getDate()+", "+now.getFullYear()+" · No. "+no+(ADV?" · Advanced":"");
var dkey=now.getFullYear()+"-"+("0"+(now.getMonth()+1)).slice(-2)+"-"+("0"+now.getDate()).slice(-2);
var KEY="dnsc-one-word-v2-"+(ADV?"adv-":"")+dkey;
function load(){try{var v=localStorage.getItem(KEY);return v?JSON.parse(v):null}catch(e){return null}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
var RX=new RegExp("^[A-Z]{"+L+"}$"),SX=new RegExp("^[ren]{"+L+"}$");
var st=load();
if(!st||!Array.isArray(st.g)||!Array.isArray(st.s))st={g:[],s:[]};
var n0=Math.min(st.g.length,st.s.length);st.g=st.g.slice(0,n0);st.s=st.s.slice(0,n0);
for(var k=0;k<st.g.length;k++){if(!RX.test(st.g[k])||!SX.test(st.s[k])){st.g=st.g.slice(0,k);st.s=st.s.slice(0,k);break}}
var cur="",busy=false,done=false;
var reduce=false;try{reduce=matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){}
var SAY={r:"right spot",e:"elsewhere",n:"not in the word"};

/* ---------- board sizing ---------- */
document.getElementById("howL").textContent=NUMW[L];
document.documentElement.style.setProperty("--tile","min("+(ADV?54:58)+"px,calc((100vw - 36px - "+((L-1)*6)+"px)/"+L+"))");
var rowsEl=document.getElementById("rows"),tiles=[];
rowsEl.setAttribute("aria-label",cap(NUMW[TR])+" rows of "+NUMW[L]+" letters");
rowsEl.style.gridTemplateRows="repeat("+TR+",var(--tile))";
for(var r=0;r<TR;r++){
  var row=document.createElement("div");row.className="row";row.style.gridTemplateColumns="repeat("+L+",var(--tile))";row.setAttribute("aria-label","Row "+(r+1));tiles.push([]);
  for(var c=0;c<L;c++){var t=document.createElement("div");t.className="t";row.appendChild(t);tiles[r].push(t)}
  rowsEl.appendChild(row);
}

/* ---------- on-screen keyboard ---------- */
var kb=document.getElementById("kb"),keys={};
["QWERTYUIOP","ASDFGHJKL",">ZXCVBNM<"].forEach(function(line){
  var d=document.createElement("div");d.className="kr";
  line.split("").forEach(function(ch){
    var k=document.createElement("button");k.type="button";k.className="key";
    if(ch===">"){k.className+=" wide";k.textContent="Enter";k.setAttribute("aria-label","Enter guess")}
    else if(ch==="<"){k.className+=" wide bk";k.textContent="⌫";k.setAttribute("aria-label","Back")}
    else{k.textContent=ch;k.setAttribute("aria-label",ch);keys[ch]=k}
    k.addEventListener("click",function(){if(ch===">")enter();else if(ch==="<")back();else typeL(ch)});
    d.appendChild(k);
  });kb.appendChild(d);
});
var RANK={n:1,e:2,r:3};
function paintKeys(){
  var best={};
  st.g.forEach(function(g,j){var s=st.s[j];for(var i=0;i<L;i++){if(!best[g[i]]||RANK[s[i]]>RANK[best[g[i]]])best[g[i]]=s[i]}});
  for(var ch in keys){var k=keys[ch],s=best[ch];k.classList.toggle("r",s==="r");k.classList.toggle("e",s==="e");k.classList.toggle("n",s==="n");
    k.setAttribute("aria-label",ch+(s?", "+SAY[s]:""))}
}

/* ---------- painting ---------- */
function setTile(t,ch,s){t.textContent=ch||"";t.classList.toggle("full",!!ch&&!s);t.classList.remove("r","e","n");if(s)t.classList.add(s)}
function paintAll(){
  for(var r=0;r<TR;r++){
    var g=st.g[r],s=st.s[r];
    for(var c=0;c<L;c++){
      if(g)setTile(tiles[r][c],g[c],s[c]);
      else if(r===st.g.length&&!done)setTile(tiles[r][c],cur[c],null);
      else setTile(tiles[r][c],"",null);
    }
  }
  paintKeys();
}
function note(t){document.getElementById("note").textContent=t}
function live(t){var l=document.getElementById("live");l.textContent="";setTimeout(function(){l.textContent=t},30)}
function sayRow(g,s){return g.split("").map(function(ch,i){return ch+" "+SAY[s[i]]}).join(", ")}

/* ---------- moves ---------- */
function typeL(ch){
  if(done||busy||cur.length>=L)return;
  if(!st.t0){st.t0=Date.now();save()}
  cur+=ch;note("");
  var t=tiles[st.g.length][cur.length-1];setTile(t,ch,null);
  if(!reduce){t.classList.remove("pop");void t.offsetWidth;t.classList.add("pop")}
}
function back(){if(done||busy||!cur.length)return;cur=cur.slice(0,-1);setTile(tiles[st.g.length][cur.length],"",null);note("")}
function enter(){
  if(done||busy)return;
  if(cur.length<L){note(cur.length?cap(NUMW[L])+" letters, please. "+(L-cur.length)+" more to go.":"Type a "+NUMW[L]+" letter word first.");return}
  var g=cur,r=st.g.length;busy=true;note("");
  fetch(API+"/guess",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ed:ED,day:dayIdx,rows:st.g.concat([g])})})
  .then(function(res){return res.json().then(function(x){return{ok:res.ok,x:x}})})
  .then(function(o){
    if(!o.ok||!o.x||!SX.test(o.x.s||"")){busy=false;note((o.x&&o.x.error)||"That one didn't go through. Try again.");return}
    var s=o.x.s;st.g.push(g);st.s.push(s);cur="";
    if(o.x.over){st.word=o.x.word;st.teach=o.x.teach;st.won=!!o.x.solved}
    save();flip(r,g,s,o.x);
  })
  .catch(function(){busy=false;note("Couldn't reach The Well. Check your connection and try again.")});
}
function flip(r,g,s,x){
  var step=reduce?90:260,half=reduce?0:250;
  tiles[r].forEach(function(t,i){
    setTimeout(function(){t.classList.remove("turn","fade");void t.offsetWidth;t.classList.add(reduce?"fade":"turn");setTimeout(function(){setTile(t,g[i],s[i])},half)},i*step);
  });
  setTimeout(function(){
    busy=false;paintKeys();
    var msg="Row "+(r+1)+": "+sayRow(g,s)+".";
    if(x.solved){
      if(!reduce)tiles[r].forEach(function(t,i){setTimeout(function(){t.classList.remove("turn");void t.offsetWidth;t.classList.add("lift")},i*90)});
      finish(true,msg);
    }else if(x.over)finish(true,msg);
    else live(msg+" "+(TR-st.g.length)+(TR-st.g.length===1?" try left.":" tries left."));
  },(L-1)*step+(reduce?360:520));
}
function finish(fresh,lead){
  try{if(window.wellSense)wellSense.play("chime")}catch(e){}
  done=true;
  var won=!!st.won;
  document.getElementById("doneK").textContent=won?"You found it":"Today's word";
  document.getElementById("doneH").textContent=st.word||"";
  document.getElementById("doneP").textContent=st.teach||"";
  note(won?"Well found.":cap(NUMW[TR])+" tries spent. Here is the word.");
  if(!st.t1){st.t1=Date.now();save()}
  var d=document.getElementById("done");d.classList.add("show");
  board(won);
  if(fresh){
    live((lead?lead+" ":"")+(won?"You found it. ":"The word was ")+st.word+". "+(st.teach||"")+" Come back tomorrow for the next word.");
    if(d.scrollIntoView)setTimeout(function(){d.scrollIntoView({behavior:reduce?"auto":"smooth",block:"nearest"})},reduce?0:700);
  }
}

/* ---------- the daily board: anonymous, opt-in, generated names only ---------- */
var NM=window.WELL_NAMES||{A:["Wobbly"],N:["Pickle"]};
function pick(a){return a[Math.floor(Math.random()*a.length)]}
function newName(){return pick(NM.A)+" "+pick(NM.N)}
function nmOk(n){var x=(n||"").split(" ");return x.length===2&&NM.A.indexOf(x[0])>=0&&NM.N.indexOf(x[1])>=0}
function device(){try{var d=localStorage.getItem("dnsc-well-device");if(!d){d=(window.crypto&&crypto.randomUUID?crypto.randomUUID():String(Math.random()).slice(2)+Date.now());localStorage.setItem("dnsc-well-device",d)}return d}catch(e){return "anon-"+dayIdx}}
function fmtT(ms){if(!(ms>0))return "";var s=Math.round(ms/1000),m=Math.floor(s/60);return m?m+"m "+("0"+(s%60)).slice(-2)+"s":s+"s"}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function showBoard(j){
  var ol=document.getElementById("lbList"),rows=(j&&j.rows)||[],me=j&&j.me,total=(j&&j.total)||0;
  if(!rows.length){ol.innerHTML='<li class="empty">No one on the board yet today. Be the first.</li>'}
  else ol.innerHTML=rows.map(function(x,i){var mine=me&&i+1===me.rank;return '<li'+(mine?' class="me"':'')+'><span>'+esc(x.name)+'</span><span class="g">'+x.guesses+'/'+TR+'</span><span class="s">'+fmtT(x.ms)+'</span></li>'}).join("");
  var you=document.getElementById("lbYou");
  if(me){you.hidden=false;you.innerHTML='<b>'+esc(me.name)+'</b> · #'+me.rank+' of '+total.toLocaleString()+' today'}else you.hidden=true;
}
function loadBoard(){
  fetch(API+"/board?ed="+ED+"&day="+dayIdx+"&device="+encodeURIComponent(device())).then(function(r){return r.json()}).then(showBoard)
  .catch(function(){document.getElementById("lbMsg").textContent="The board is resting. Try again in a bit."});
}
function board(won){
  var lb=document.getElementById("lb");lb.hidden=false;
  document.getElementById("lbEd").textContent=ADV?"Advanced":"Regular";
  var j=document.getElementById("join"),msg=document.getElementById("lbMsg");
  if(won&&!st.posted&&!st.skipped){
    if(!nmOk(st.name)){st.name=newName();save()}
    j.hidden=false;document.getElementById("nm").textContent=st.name;
    document.getElementById("reroll").onclick=function(){st.name=newName();save();document.getElementById("nm").textContent=st.name};
    document.getElementById("skip").onclick=function(){st.skipped=true;save();j.hidden=true};
    document.getElementById("submit").onclick=function(){
      var b=this;b.disabled=true;msg.textContent="Adding you…";
      fetch(API+"/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ed:ED,day:dayIdx,rows:st.g,ms:(st.t1&&st.t0)?st.t1-st.t0:0,name:st.name,device:device()})})
      .then(function(r){return r.json().then(function(x){return{ok:r.ok,status:r.status,x:x}})})
      .then(function(o){
        if(o.ok||o.status===409){st.posted=true;save();j.hidden=true;msg.textContent="";showBoard(o.x)}
        else{b.disabled=false;msg.textContent=o.x.error||"That didn't go through. Try again."}
      })
      .catch(function(){b.disabled=false;msg.textContent="The board is resting. Try again in a bit."});
    };
  }else j.hidden=true;
  loadBoard();
}

/* ---------- physical keyboard ---------- */
document.addEventListener("keydown",function(ev){
  if(ev.metaKey||ev.ctrlKey||ev.altKey)return;
  var t=ev.target,k=ev.key;
  if(t&&t.closest&&t.closest("a,.site-nav,.site-foot,.lb"))return;
  var onKey=!!(t&&t.classList&&t.classList.contains("key"));
  if(t&&t.tagName==="BUTTON"&&!onKey&&(k==="Enter"||k===" "))return;
  if(/^[a-z]$/i.test(k)){ev.preventDefault();typeL(k.toUpperCase())}
  else if(k==="Backspace"||k==="Delete"){ev.preventDefault();back()}
  else if(k==="Enter"){ev.preventDefault();enter()}
});

/* ---------- start ---------- */
paintAll();
document.getElementById("lbEd").textContent=ADV?"Advanced":"Regular";
if(st.word&&(st.won||st.g.length>=TR))finish(false);
else{loadBoard();if(st.g.length)live("Welcome back. "+st.g.length+(st.g.length===1?" guess":" guesses")+" so far. "+st.g.map(function(g,i){return "Row "+(i+1)+": "+sayRow(g,st.s[i])}).join(". ")+".")}
})();

/* the little things floating around: a few gold and sky motes, slow, paper-light */
(function(){
  var cv=document.getElementById("motes");if(!cv||!cv.getContext)return;
  var cx=cv.getContext("2d"),reduce=false;try{reduce=matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){}
  var W,H,dpr,motes=[],COLS=["217,178,90","62,106,158","180,134,46","166,150,134"];
  function size(){dpr=window.devicePixelRatio||1;W=cv.width=innerWidth*dpr;H=cv.height=innerHeight*dpr;cv.style.width=innerWidth+"px";cv.style.height=innerHeight+"px";
    motes=[];for(var i=0,n=Math.round(innerWidth/28);i<n;i++)motes.push({x:Math.random()*W,y:Math.random()*H,r:(Math.random()*1.6+.8)*dpr,v:(Math.random()*.18+.06)*dpr,w:Math.random()*Math.PI*2,c:COLS[Math.floor(Math.random()*COLS.length)],o:Math.random()*.35+.15})}
  function draw(t){cx.clearRect(0,0,W,H);
    for(var i=0;i<motes.length;i++){var m=motes[i];if(!reduce){m.y-=m.v;m.x+=Math.sin(t/3200+m.w)*.2*dpr;if(m.y<-10){m.y=H+10;m.x=Math.random()*W}}
      cx.beginPath();cx.arc(m.x,m.y,m.r,0,Math.PI*2);cx.fillStyle="rgba("+m.c+","+(m.o*(.65+.35*Math.sin(t/2200+m.w)))+")";cx.fill()}
    if(!reduce)requestAnimationFrame(draw)}
  addEventListener("resize",size);size();requestAnimationFrame(draw);
})();
