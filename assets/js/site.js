const $=id=>document.getElementById(id),RM=matchMedia('(prefers-reduced-motion:reduce)').matches,TG='https://t.me/sahilsleem',MAIL='mailto:examstash1@gmail.com';
const IC={tg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 3 2.5 10.4l6 2.3 2.3 6.2 3.2-4 4.8 3.6z"/><path d="m8.5 12.7 13-9.7"/></svg>',ig:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',ml:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'};

let hero,io,metaT;
function fit(){const e=document.querySelector('.eye');if(!e)return;let f=12.5;e.style.fontSize=f+'px';while(e.scrollWidth>e.clientWidth+1&&f>8){f-=.25;e.style.fontSize=f+'px'}}

function post(){
  hero=$('hero');fit();const h1=$('h1');
  if(h1&&!RM){
    if(!h1.dataset.split) {
      h1.dataset.split = "1";
      let i=0;h1.setAttribute('aria-label',h1.textContent);h1.innerHTML=h1.innerHTML.split(' ').map(w=>w.startsWith('&')&&w.length<6?w:'<span class="wd" aria-hidden="true">'+(w.includes('&amp;')?w:[...w].map(ch=>`<span class="ch" style="--i:${Math.min(i++,26)}">${ch}</span>`).join(''))+'</span>').join(' ');
    }
  }
  if(io){document.querySelectorAll('.rv:not(.in)').forEach(e=>io.observe(e));}

  const q=$('q');
  const dd=$('dd');
  if(q&&dd){
    q.addEventListener('input',()=>{
      const v=q.value.trim().toLowerCase();if(!v){dd.hidden=true;return}
      const data = window.EXAMSTASH_SEARCH_INDEX || [];
      let m=data.filter(x=>(x.title+' '+x.keywords).toLowerCase().includes(v)).slice(0,6);
      dd.innerHTML=m.length?m.map(x=>`<a href="${x.url}"><b>${x.title}</b><small>${x.category || ''}</small></a>`).join(''):'<p>No matching course. Try another name.</p>';
      dd.hidden=false;
    });
    q.addEventListener('keydown',e=>{
      if(e.key==='Enter'&&!dd.hidden&&dd.querySelector('a')&&q.value.trim()){
        location.href=dd.querySelector('a').href;
      }
      if(e.key==='Escape')dd.hidden=true;
    });
    document.addEventListener('click',e=>{if(!e.target.closest('.sw'))dd.hidden=true});
  }
  const hm=$('hm'),menu=$('menu');
  if(hm&&menu){
    const closeMenu = () => { if(!menu.hidden){menu.hidden=true;hm.setAttribute('aria-expanded','false')} };
    hm.addEventListener('click',e=>{menu.hidden=!menu.hidden;hm.setAttribute('aria-expanded',!menu.hidden);e.stopPropagation()});
    document.addEventListener('click',e=>{if(!e.target.closest('.h-nav'))closeMenu()});
    window.addEventListener('scroll',closeMenu,{passive:true});
  }
}

/* ---------- colour field + ink ---------- */
const hex=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)/255);
const PAL=['#ffffff','#c9f7e6','#ffffff','#cfe8ff','#2f5bff','#ffffff','#fff2b3','#ffffff','#e0d4ff','#0e7490','#ffffff','#ffd9b3','#ffffff','#6a4cff','#111827'].map(hex);
const sm=(a,b,x)=>{x=Math.max(0,Math.min(1,(x-a)/(b-a)));return x*x*(3-2*x)};
const lin=c=>c<=.04045?c/12.92:Math.pow((c+.055)/1.055,2.4),Lm=c=>.2126*lin(c[0])+.7152*lin(c[1])+.0722*lin(c[2]);
const css=c=>'rgb('+c.map(v=>Math.round(v*255)).join(',')+')';
const hx=c=>'#'+c.map(v=>Math.round(v*255).toString(16).padStart(2,'0')).join('');
let inkB=true;
function setInk(b){inkB=b;const s=document.documentElement.style;s.setProperty('--ink',b?'#0b0d12':'#ffffff');s.setProperty('--inv',b?'#ffffff':'#0b0d12')}
function colAt(T){const s=T/4,i=Math.floor(s),f=s-i,e=sm(.3,1,f),a=PAL[i%PAL.length],b=PAL[(i+1)%PAL.length];return[a.map((v,j)=>v+(b[j]-v)*e),b]}
const BFS=`uniform float t;uniform vec2 r;uniform vec3 a,b;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}
void main(){vec2 u=gl_FragCoord.xy/r;vec2 p=u*vec2(r.x/r.y,1.)*1.8;
p+=.35*vec2(n(p+vec2(t*.12,0.)),n(p.yx+vec2(0.,t*.1)));
float q=n(p*1.3+vec2(t*.05,0.));
float m=smoothstep(.35,.85,n(p*.8+vec2(t*.06,-t*.05)));
vec3 c=mix(a*(.96+.06*q),b,.22*m);gl_FragColor=vec4(c,1.);}`;
let T=0,pt=0,px=0,py=0,tx=0,ty=0,bgt=0,R,U,sc3,cam;
function initBG(){
  const c=$('bg');if(!c)return;
  if(typeof THREE==='undefined') return;
  try{
    R=new THREE.WebGLRenderer({canvas:c,powerPreference:'low-power',alpha:true});R.setPixelRatio(1);
    sc3=new THREE.Scene();cam=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
    U={t:{value:0},r:{value:new THREE.Vector2()},a:{value:new THREE.Vector3(1,1,1)},b:{value:new THREE.Vector3(1,1,1)}};
    const bm=new THREE.Mesh(new THREE.PlaneGeometry(2,2),new THREE.ShaderMaterial({uniforms:U,vertexShader:'void main(){gl_Position=vec4(position.xy,0.,1.);}',fragmentShader:BFS}));
    bm.frustumCulled=false;sc3.add(bm);
    const rs=()=>{R.setSize(innerWidth,innerHeight,false);R.getDrawingBufferSize(U.r.value)};rs();addEventListener('resize',rs);
  }catch(e){}
}
function frame(now){
  requestAnimationFrame(frame);if(document.hidden)return;
  const dt=Math.min((now-pt)/1000,.1);pt=now;if(!RM)T+=dt;
  const[c,nx]=colAt(T),L1=Lm(c),L2=Lm(c.map((v,j)=>v+(nx[j]-v)*.22)),kb=(Math.min(L1,L2)+.05)/.05,kw=1.05/(Math.max(L1,L2)+.05),wb=inkB?kb*1.1>=kw:kb>kw*1.1;if(wb!==inkB)setInk(wb);
  if(now-bgt>120){
    bgt=now;
    document.body.style.backgroundColor=css(c);
    document.documentElement.style.setProperty('--page', css(c));
    if(metaT)metaT.content=hx(c);
  }
  tx+=(px-tx)*.06;ty+=(py-ty)*.06;
  if(hero)hero.style.transform=`perspective(900px) rotateY(${tx*7}deg) rotateX(${-ty*5}deg)`;
  if(U&&R){U.t.value=T;U.a.value.set(...c);U.b.value.set(...nx);R.render(sc3,cam);}
}

document.addEventListener('DOMContentLoaded',()=>{
  metaT=document.querySelector('meta[name=theme-color]');

  // Reveal safety: 2-second timeout ensures all content is visible even if IntersectionObserver is slow
  if(typeof IntersectionObserver !== 'undefined'){
    io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08});
  }
  setTimeout(()=>{document.querySelectorAll('.rv:not(.in)').forEach(e=>e.classList.add('in'))},2000);

  addEventListener('pointermove',e=>{px=e.clientX/innerWidth-.5;py=e.clientY/innerHeight-.5},{passive:true});
  addEventListener('deviceorientation',e=>{if(e.gamma==null)return;px=Math.max(-.5,Math.min(.5,e.gamma/60));py=Math.max(-.5,Math.min(.5,((e.beta||45)-45)/60))});
  const rst=c=>{c.style.setProperty('--rx','0deg');c.style.setProperty('--ry','0deg');c.style.setProperty('--z','0px')};
  document.addEventListener('pointermove',e=>{
    const c=e.target.closest&&e.target.closest('.card,.tilt');if(!c||RM)return;
    const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
    c.style.setProperty('--rx',(-y*16)+'deg');c.style.setProperty('--ry',(x*16)+'deg');c.style.setProperty('--z','26px');
  });
  ['pointerout','pointerup','pointercancel'].forEach(ev=>document.addEventListener(ev,e=>{
    const c=e.target.closest&&e.target.closest('.card,.tilt');if(c)rst(c);
  }));

  const soc = $('soc');
  if(soc) soc.innerHTML=[[TG,'Telegram',IC.tg],['https://www.instagram.com/sahilsleem/','Instagram',IC.ig],[MAIL,'Email',IC.ml]].map(x=>`<a href="${x[0]}" aria-label="${x[1]}" title="${x[1]}">${x[2]}</a>`).join('');

  addEventListener('resize',fit);if(document.fonts)document.fonts.ready.then(fit);
  post();
  initBG();
  requestAnimationFrame(frame);
});
