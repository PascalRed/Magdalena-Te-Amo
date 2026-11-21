"""Mi amorrrr, si lees esto, no crees que debes aceptar lo mucho que te amo?
TE AMO MAGDALENA"""
import math, random, base64, os
from array import array

random.seed(11)
PI = math.pi
V = lambda a, b: [a[i] - b[i] for i in range(3)]
def norm(a):
    n = math.sqrt(sum(x * x for x in a)) or 1
    return [x / n for x in a]
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def basis(d, roll=0.0):
    d = norm(d); t = [1, 0, 0] if abs(d[0]) < .9 else [0, 0, 1]
    x = norm(cross(t, d)); z = cross(d, x)
    c, s = math.cos(roll), math.sin(roll)
    x2 = [c*x[i] + s*z[i] for i in range(3)]
    return x2, d, cross(d, x2)
ID = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
def place(p, B, o): return [o[i] + sum(p[k]*B[k][i] for k in range(3)) for i in range(3)]
def rot(n, B): return [sum(n[k]*B[k][i] for k in range(3)) for i in range(3)]

PAL, PTS = [], []
def ix(rgb):
    if rgb not in PAL: PAL.append(rgb)
    return PAL.index(rgb)
def dark(rgb, f=.5): return tuple(int(c*f) for c in rgb)
def add(q, n, ci, t=1.0):
    PTS.append([q[0]*1000, q[1]*1000, q[2]*1000, n[0]*100, n[1]*100, n[2]*100, ci, t*100])

def surf(f, nu, nv, B, o, tone, e=1e-3):
    for i in range(nu):
        for j in range(nv):
            u = (i + random.random()*.8) / nu
            v = -1 + 2*(j + random.random()*.8) / nv
            pu = V(f(u+e, v), f(u-e, v)); pv = V(f(u, v+e), f(u, v-e))
            n = norm(cross(pu, pv)); ci, t = tone(u, v)
            add(place(f(u, v), B, o), rot(n, B), ci, t)

def petal(o, B, ph, L, W, a0, a1, ci, spot=None, pw=.8, sw=.8, cup=.4):
    def f(u, v):
        a = a0 + a1*u
        r = L*(math.cos(a0) - math.cos(a))/a1
        h = L*(math.sin(a) - math.sin(a0))/a1
        w = W*abs(math.sin(PI*min(max(u, 0), 1)**pw))**sw; l = v*w
        return [r*math.cos(ph) - l*math.sin(ph), h - cup*w*v*v, r*math.sin(ph) + l*math.cos(ph)]
    def tone(u, v):
        if spot is not None and .12 < u < .6 and random.random() < .07: return spot, .9
        return ci, 1 - .28*math.exp(-v*v*7) + .1*u
    surf(f, int(L/.016)+2, int(W*2/.016)+2, B, o, tone)

STAM, ANTH, YEL = ix((235, 200, 120)), ix((130, 55, 30)), ix((255, 210, 40))

def lily(o, d, roll, L, rgb):
    B = basis(d, roll); ci = ix(rgb); sp = ix(dark(rgb, .5))
    for k in range(6):
        inner = k % 2 == 0
        petal(o, B, k*PI/3, L*(.92 if inner else 1), L*(.27 if inner else .22),
              .3 if inner else .5, .9 if inner else 1.3, ci, sp)
    for k in range(6):
        ph = k*PI/3 + .5
        for s in range(26):
            t = s/25; r = .32*L*t
            add(place([r*math.cos(ph), .7*L*t - .1*L*t*t, r*math.sin(ph)], B, o),
                rot([math.cos(ph), 0, math.sin(ph)], B), STAM, 1)
        tip = [.32*L*math.cos(ph), .6*L, .32*L*math.sin(ph)]
        for _ in range(14):
            p = [tip[i] + random.uniform(-.025, .025) for i in range(3)]
            add(place(p, B, o), rot(norm([random.uniform(-1, 1) for _ in range(3)]), B), ANTH, 1)

def rose(o, d, roll, R, rgb):
    B = basis(d, roll); ci = ix(rgb)
    for l in range(6):
        n = 3 if l < 2 else 5; Rl = R*(.4 + .12*l); p0 = .12*l; p1 = .8 + .2*l
        span = PI/n*1.35
        for k in range(n):
            th0 = l*2.4 + k*2*PI/n
            def f(u, v):
                ph = p0 + (p1 - p0)*(1 - .25*v*v)*u; th = th0 + v*span*(1 - .3*u*u)
                rr = Rl*(1 + .3*u**3)
                return [rr*math.sin(ph)*math.cos(th), rr*math.cos(ph), rr*math.sin(ph)*math.sin(th)]
            surf(f, int(Rl*(p1-p0)/.015)+3, int(Rl*span*2/.015)+3, B, o, lambda u, v: (ci, .55 + .5*u))

def blossom(o, d, roll, L, rgb, center=YEL):
    B = basis(d, roll); ci = ix(rgb)
    for k in range(5):
        petal(o, B, k*2*PI/5, L, L*.42, 1.15, .35, ci, None, pw=.55, sw=.6, cup=.2)
    for _ in range(45):
        a, r = random.uniform(0, 2*PI), L*.14*math.sqrt(random.random())
        add(place([r*math.cos(a), .04, r*math.sin(a)], B, o), rot([0, 1, 0], B), center, 1)

WHT = ix((255, 255, 255))
def gyp(o):
    for _ in range(6):
        c = [o[i] + random.uniform(-.14, .14) for i in range(3)]
        for _ in range(26):
            n = norm([random.uniform(-1, 1) for _ in range(3)])
            add([c[i] + n[i]*.05*random.random()**.5 for i in range(3)], n, WHT, .9)

G1, G2 = ix((60, 170, 85)), ix((35, 125, 65))
def stem(a, b, rad, ci=G1, step=.02, ring=5, bend=.08):
    d = V(b, a); Ln = math.sqrt(sum(x*x for x in d)); B = basis(d, 0)
    m = [(a[i]+b[i])/2 + random.uniform(-bend, bend) for i in range(3)]
    for i in range(int(Ln/step)+1):
        t = i/int(Ln/step)
        c = [(1-t)**2*a[k] + 2*(1-t)*t*m[k] + t*t*b[k] for k in range(3)]
        for j in range(ring):
            an = j*2*PI/ring; nl = rot([math.cos(an), 0, math.sin(an)], B)
            add([c[k] + rad*nl[k] for k in range(3)], nl, ci, 1)

def leaf(F, psi, L):
    od, tg = [math.cos(psi), 0, math.sin(psi)], [-math.sin(psi), 0, math.cos(psi)]
    def f(u, v):
        r = L*.9*u; h = L*(.9*u - .8*u*u)
        w = .17*abs(math.sin(PI*min(max(u, 0), 1)**.7))**.8; l = v*w
        return [r*od[0] + l*tg[0], h - .3*w*v*v, r*od[2] + l*tg[2]]
    surf(f, int(L/.016)+2, 22, ID, [F[0], F[1] + .05, F[2]], lambda u, v: (G2, 1 - .3*math.exp(-v*v*8)))

pol = lambda r, y, p: [r*math.cos(p), y, r*math.sin(p)]
F = [0, -1.1, 0]
def head(p, fn, *a):
    d = norm(V(p, F)); d = norm([d[0]+random.uniform(-.08, .08), d[1], d[2]+random.uniform(-.08, .08)])
    stem([F[0]+random.uniform(-.05, .05), F[1], F[2]+random.uniform(-.05, .05)], [p[i]-d[i]*.04 for i in range(3)], .016)
    fn(p, d, random.uniform(0, 2*PI), *a)

for k in range(7): leaf(F, k*2*PI/7 + .3, 1.35)
for p, L, c in [(pol(0, .85, 0), .62, (255, 232, 205)), (pol(.8, .45, .4), .55, (245, 105, 185)),
                (pol(.85, .35, 2.0), .55, (230, 40, 55)), (pol(.8, .4, 3.6), .55, (250, 205, 60)),
                (pol(.8, .4, 5.1), .55, (185, 75, 175))]:
    head(p, lily, L, c)
for k, c in enumerate([(255, 115, 150), (205, 25, 60), (255, 170, 140), (255, 205, 220)]):
    head(pol(.6, -.05, 1.2 + k*1.57), rose, .27, c)
cols = [(165, 140, 255), (255, 255, 255), (110, 170, 255), (255, 150, 60)]
for k in range(9):
    head(pol(random.uniform(.95, 1.1), random.uniform(-.4, .1), k*2*PI/9 + .2), blossom, .2, cols[k % 4])
for k in range(3):
    head(pol(.4, .98, k*2*PI/3 + 1), blossom, .17, cols[(k+1) % 4])
for k in range(10):
    p = pol(random.uniform(.8, 1.2), random.uniform(.2, .75), k*2*PI/10 + .5)
    stem(F, p, .01, G2, .03, 4); gyp(p)

stem(F, [0, -2.15, 0], .1, G1, .02, 16, .0)
RB = ix((240, 225, 205))
stem([0, -1.42, 0], [0, -1.6, 0], .118, RB, .01, 22, .0)

pk = array('h')
for p in PTS: pk.extend(int(round(x)) for x in p)
data = base64.b64encode(pk.tobytes()).decode()

HTML = r'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Bouquet ASCII PARA MI NOVIAA</title>
<style>:root{color-scheme:dark;--bg:#000}html,body{margin:0;height:100%;background:var(--bg);overflow:hidden}
canvas{display:block;touch-action:none;cursor:grab}canvas:active{cursor:grabbing}</style></head>
<body><canvas id="c"></canvas><script>
const D="__DATA__",PAL=__PAL__;
const P=new Int16Array(Uint8Array.from(atob(D),c=>c.charCodeAt(0)).buffer),N=P.length/8;
const X=new Float32Array(N),Y=new Float32Array(N),Z=new Float32Array(N),NX=new Float32Array(N),NY=new Float32Array(N),NZ=new Float32Array(N),C=new Uint8Array(N),T=new Float32Array(N);
for(let i=0;i<N;i++){const o=i*8;X[i]=P[o]/1000;Y[i]=P[o+1]/1000+.3;Z[i]=P[o+2]/1000;NX[i]=P[o+3]/100;NY[i]=P[o+4]/100;NZ[i]=P[o+5]/100;C[i]=P[o+6];T[i]=P[o+7]/100}
const cv=document.getElementById('c'),g=cv.getContext('2d'),RAMP=".:-=+*#%@",LX=-.35,LY=.55,LZ=.76;
let W,H,S,cw,ch,cols,rows,dep,idx,stars=[];
function size(){const r=devicePixelRatio||1;W=innerWidth;H=innerHeight;cv.width=W*r;cv.height=H*r;g.setTransform(r,0,0,r,0,0);
 S=Math.min(H*.8/4.6,W*.92/2.9);ch=Math.max(6,S*.045);cw=ch*.55;cols=Math.ceil(W/cw);rows=Math.ceil(H/ch);
 dep=new Float32Array(cols*rows);idx=new Int32Array(cols*rows);
 stars=Array.from({length:Math.round(W*H/5500)},()=>({x:Math.random()*W,y:Math.random()*H,r:.5+Math.random()*.9,p:Math.random()*6.28,s:.4+Math.random()*1.2}))}
addEventListener('resize',size);size();
const AUTO=-.0055;let ang=0,pit=.14,vel=AUTO,drag=false,lx=0,ly=0,last=performance.now();
cv.addEventListener('pointerdown',e=>{drag=true;lx=e.clientX;ly=e.clientY;cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-lx,dy=e.clientY-ly;lx=e.clientX;ly=e.clientY;
 ang+=dx*.009;vel=dx*.009;pit=Math.max(-.5,Math.min(.8,pit+dy*.005))});
const up=()=>{drag=false};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
function frame(t){const dt=Math.min(50,t-last)/16.7;last=t;
 if(!drag){vel+=(AUTO-vel)*.03*dt;ang+=vel*dt}else vel*=.8;
 const ca=Math.cos(ang),sa=Math.sin(ang),cp=Math.cos(pit),sp=Math.sin(pit);
 g.fillStyle='#000';g.fillRect(0,0,W,H);
 for(const s of stars){g.globalAlpha=.25+.75*(.5+.5*Math.sin(t*.001*s.s+s.p));g.fillStyle='#fff';g.beginPath();g.arc(s.x,s.y,s.r,0,6.283);g.fill()}
 g.globalAlpha=1;dep.fill(-1e9);idx.fill(-1);const cx=W/2,cy=H/2;
 for(let i=0;i<N;i++){const x=X[i],y=Y[i],z=Z[i];const x1=x*ca+z*sa,z1=-x*sa+z*ca,y1=y*cp-z1*sp,z2=y*sp+z1*cp;
  const f=7/(7-z2),c=(cx+x1*f*S)/cw|0,r=(cy-y1*f*S)/ch|0;if(c<0||r<0||c>=cols||r>=rows)continue;
  const k=r*cols+c;if(z2>dep[k]){dep[k]=z2;idx[k]=i}}
 g.font=(ch*.98)+'px ui-monospace,Menlo,Consolas,monospace';g.textBaseline='alphabetic';
 for(let k=0;k<idx.length;k++){const i=idx[k];if(i<0)continue;
  const nx=NX[i],ny=NY[i],nz=NZ[i];let a=nx*ca+nz*sa,b=-nx*sa+nz*ca,n2=ny*cp-b*sp,n3=ny*sp+b*cp;
  if(n3<0){a=-a;n2=-n2;n3=-n3}
  const l=Math.max(0,Math.min(1,.3+.75*Math.max(0,a*LX+n2*LY+n3*LZ)))*(.8+.2*Math.min(1,(dep[k]+1.3)/2.6));
  const p=PAL[C[i]],m=T[i]*(.5+.8*l);
  g.fillStyle=`rgb(${Math.min(255,p[0]*m)|0},${Math.min(255,p[1]*m)|0},${Math.min(255,p[2]*m)|0})`;
  g.fillText(RAMP[Math.min(8,l*9|0)],(k%cols)*cw,((k/cols|0)+1)*ch*.92)}
 requestAnimationFrame(frame)}
requestAnimationFrame(frame);
</script></body></html>'''

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bouquet.html")
open(out, "w", encoding="utf-8").write(
    HTML.replace("__DATA__", data).replace("__PAL__", str([list(c) for c in PAL])))
print(len(PTS), "puntos ->", out, round(os.path.getsize(out)/1e6, 2), "MB")
