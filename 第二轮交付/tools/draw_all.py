#!/usr/bin/env python3
"""Regenerate all 24 editable figures. Standard-library geometry; Inkscape renders.
All numeric drawing/model parameters are illustrative, not recovered exam data.
"""
from pathlib import Path
import math, json, sys, subprocess, os, hashlib, csv
from html import escape
from draw_prisms import SVG, INK, ACCENT, CAUTION, make_2021, make_2025, make_2026
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'SVG'
AUDIT={}

def fig(h,title,desc='示意位置不代表原题数值；透明背景，可编辑路径与文字。'):
 s=SVG(h,title,desc);s.text(35,45,title,'heading');return s

def raw(s,d,cls='',extra=''):
 s.parts.append(f'<path class="line {cls}" d="{d}" {extra}/>')

def rect(s,x,y,w,h,cls=''):
 s.path([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],cls)

def dim(s,x1,x2,y,label):
 s.path([(x1,y),(x2,y)],arrow=True,both=True)
 for x in [x1,x2]:s.path([(x,y-9),(x,y+9)])
 s.text((x1+x2)/2,y+36,label,'note','middle')

def dot(s,x,y,label='',dx=0,dy=30,cls=''):
 s.circle(x,y,2.4,fill=ACCENT if cls else INK)
 if label:s.text(x+dx,y+dy,label,cls or 'math','middle')

def arrow(s,p,cls='ray'):
 # One mid-segment arrow preserves the unobstructed endpoint/optical element.
 s.path(p,cls)
 if len(p)>1:
  a,b=p[-2:];u=(a[0]*.58+b[0]*.42,a[1]*.58+b[1]*.42);v=(a[0]*.42+b[0]*.58,a[1]*.42+b[1]*.58)
  s.path([u,v],cls,True)

def labelbox(s,y,lines):
 for i,line in enumerate(lines):s.text(40,y+43*i,line,'note')

def lens(s,x,y,h,label,positive=True):
 s.path([(x,y-h),(x,y+h)])
 if positive:
  for sign in [-1,1]:s.path([(x-6,y+sign*(h-10)),(x,y+sign*h),(x+6,y+sign*(h-10))])
 s.text(x,y-h-20,label,'math','middle')

def stop(s,x,y,h,H,label='Q'):
 s.path([(x,y-H),(x,y-h)]);s.path([(x,y+h),(x,y+H)])
 dot(s,x,y,label,dx=19,dy=32)

def cavity():
 s=fig(755,'2016 / 两镜腔选项')
 for i,(xx,yy) in enumerate([(45,115),(480,115),(45,410),(480,410)]):
  l,r=xx+75,xx+290;c=yy+80
  s.text(xx,yy,'ABCD'[i],'heading')
  s.path([(xx+30,c),(xx+340,c)],dash=True)
  raw(s,f'M {l+18} {c-65} Q {l-18} {c} {l+18} {c+65}')
  if i==0:s.path([(r,c-65),(r,c+65)])
  elif i==1:raw(s,f'M {r-18} {c-65} Q {r+18} {c} {r-18} {c+65}')
  else:raw(s,f'M {r+16} {c-45} Q {r-16} {c} {r+16} {c+45}')
  s.text(l+37,c-77,'R₂' if i==2 else 'R','math')
  if i==1:s.text(r-50,c-77,'R','math')
  if i==2:s.text(r+15,c-62,'R₁','math')
  if i==3:s.text(r-38,c-70,'R − L','note')
  dim(s,l,r,c+104,['L = 0.8R','L = 0.5R','L = 0.5R₂','L = 0.5R'][i])
  if i==2:s.text(xx+175,yy+280,'R₁ < L','note','middle')
  if i==3:s.text(xx+175,yy+280,'两镜共心','note','middle')
 return s

def point():
 s=fig(430,'2016 / 点光源、透镜与衍射屏')
 s.path([(55,225),(855,225)],dash=True)
 dot(s,170,225,'S',dy=37)
 raw(s,'M 475 105 Q 437 225 475 345 Q 513 225 475 105')
 s.path([(512,105),(512,345)])
 for y in [140,310]:arrow(s,[(170,225),(454,y)])
 dim(s,170,475,373,'80 mm')
 s.text(448,84,'f = 50 mm','note','middle')
 s.text(550,151,'衍射屏','note');s.text(550,194,'t(x, y)','math')
 s.text(550,322,'紧贴透镜后表面','note')
 return s

def qswitch():
 s=fig(355,'2017 / 偏振选通式电光调 Q 腔')
 s.path([(65,190),(837,190)],dash=True)
 # Preserve original order: output mirror, gain medium, polarizer, EO crystal, mirror.
 raw(s,'M 95 122 Q 112 190 95 258');s.path([(83,122),(83,258)])
 raw(s,'M 240 164 L340 164 A12 26 0 0 1 340 216 L240 216 A12 26 0 0 1 240 164')
 raw(s,'M 240 164 A12 26 0 0 1 240 216')
 for x,w,h in [(438,58,90),(590,62,58)]:
  rect(s,x,190-h/2,w,h);s.path([(x,190-h/2),(x+13,190-h/2-13),(x+w+13,190-h/2-13),(x+w,190-h/2)])
  s.path([(x+w+13,190-h/2-13),(x+w+13,190+h/2-13),(x+w,190+h/2)])
 raw(s,'M 772 123 Q 750 190 772 257');s.path([(786,123),(786,257)])
 for x,t,y in [(91,'输出镜',99),(286,'增益介质',288),(468,'偏振器',99),(623,'电光晶体',288),(781,'反射镜',99)]:s.text(x,y,t,'note','middle')
 s.text(40,338,'位相延迟按单程定义；光在腔内往返两次通过晶体。','note')
 return s

def gain():
 s=fig(685,'2018 / 增益曲线选项（定性）')
 for i,(ox,oy) in enumerate([(60,110),(490,110),(60,400),(490,400)]):
  s.text(ox,oy-15,'ABCD'[i],'heading')
  s.path([(ox,oy+180),(ox+330,oy+180)],arrow=True)
  s.path([(ox+160,oy+200),(ox+160,oy)],arrow=True)
  s.text(ox+172,oy+9,'g','math');s.text(ox+337,oy+188,'ν','math')
  s.path([(ox+10,oy+91),(ox+312,oy+91)],dash=True);s.text(ox+8,oy+77,'g_th','note')
  curves=[
   [(10,176),(90,176),(133,160),(147,65),(154,18),(168,18),(176,65),(191,161),(235,176),(310,176)],
   [(10,176),(85,176),(119,155),(139,69),(150,27),(153,50),(160,67),(168,51),(171,27),(182,69),(203,155),(240,176),(310,176)],
   [(10,176),(80,176),(123,91),(160,91),(197,91),(240,176),(310,176)],
   [(10,176),(83,176),(126,154),(138,64),(146,28),(153,107),(160,108),(167,107),(174,28),(182,64),(194,154),(239,176),(310,176)]]
  p=curves[i];d=f'M {ox+p[0][0]} {oy+p[0][1]}'
  for k in range(1,len(p),3):d+=' C '+' '.join(f'{ox+x} {oy+y}' for x,y in p[k:k+3])
  raw(s,d,'ray')
 return s

def newton():
 s=fig(460,'牛顿环 / 球面工件与样板')
 # Both curves contact at O, upper has greater curvature (R<R0).
 raw(s,'M 180 145 L720 145 L720 215 Q450 385 180 215 Z')
 raw(s,'M 180 265 Q450 335 720 265 L720 355 L180 355 Z')
 s.path([(450,157),(450,393)],dash=True)
 dot(s,450,300,'O',dx=-22,dy=35)
 dim(s,180,720,100,'Φ')
 s.text(547,185,'R','math');s.path([(560,194),(632,259)],arrow=True)
 s.text(657,206,'R₀','math');s.path([(682,216),(685,273)],arrow=True)
 s.text(45,430,'R < R₀；空气隙在中心接触，厚度未按比例绘制。','note')
 return s

def slits():
 s=fig(440,'2020 / 交替间隔的 2N 条缝')
 a=34;xs=[80,148,284,352,488,556,760,828]
 for x in xs:rect(s,x,135,a,170)
 # Use outlined apertures, label transparent slits, do not add background fill.
 for left,right,t in [(80,114,'a'),(114,148,'a'),(148,182,'a'),(182,284,'3a')]:dim(s,left,right,95,t)
 s.text(660,227,'⋯','heading','middle')
 s.path([(97,321),(165,321)],dash=True)
 s.text(82,358,'空白长条为透光缝；相邻暗间隔依次 a、3a。','note')
 s.text(82,405,'每条缝宽 a；总缝数 2N。','note')
 return s

def double_hole():
 s=fig(395,'2023 / 双孔衍射选项')
 for x,label in [(150,'A'),(440,'B'),(735,'C')]:s.text(x,99,label,'heading','middle')
 for cx in [150,440,670,803]:
  for r in [14,32,52]:s.circle(cx,220,r)
 # Line illustrations, not a numerical intensity map. Clip stripes to outer circle.
 for cx,label in [(150,'v'),(440,'h')]:
  s.parts.append(f'<defs><clipPath id="clip-{label}"><circle cx="{cx}" cy="220" r="58"/></clipPath></defs>')
  s.parts.append(f'<g clip-path="url(#clip-{label})">')
  for j in range(-3,4):
   if label=='v':s.path([(cx+j*17,155),(cx+j*17,285)])
   else:s.path([(cx-65,220+j*17),(cx+65,220+j*17)])
  s.end()
 s.text(40,357,'原选项的方向与组合示意；不表示定量光强。','note')
 return s

def young():
 s=fig(490,'2025 / 斜入射双孔干涉')
 s.path([(60,255),(858,255)],arrow=True);s.text(864,267,'Z','math')
 # Aperture plane with two holes A and B; X axis at observation plane.
 for y1,y2 in [(90,191),(211,299),(319,370)]:s.path([(340,y1),(340,y2)])
 s.text(364,204,'A','math');s.text(364,316,'B','math');s.text(318,80,'p','math')
 for shift in [-54,0,54]:arrow(s,[(95,377+shift),(315,267+shift)])
 s.path([(715,370),(715,90)],arrow=True);s.text(731,97,'X','math')
 raw(s,'M 269 255 A70 70 0 0 0 276.4 286.3');s.text(256,308,'θ','math')
 dim(s,340,715,403,'d = 100 mm')
 s.text(42,470,'AB = 1 mm；λ = 0.5 μm；sin θ ≈ tan θ ≈ 0.1。','note')
 return s

def grating():
 s=fig(960,'闪耀光栅 / 角定义与条件')
 # Facet rises to the right; its outward normal tilts to the left by gamma.
 pts=[(90,325),(270,270),(285,325),(465,270),(480,325),(660,270),(675,325),(825,279)]
 s.path(pts,'ray');s.path([(70,325),(850,325)],dash=True)
 O=(465,270);s.path([O,(465,95)],dash=True);s.text(480,100,'栅面法线','note')
 s.path([O,(401,61)],dash=True);s.text(268,77,'槽面法线','note')
 raw(s,'M 465 179 A91 91 0 0 0 438.4 183');s.text(427,166,'γ','math')
 s.text(685,356,'栅面','note');s.text(526,285,'槽面','note')
 dim(s,285,480,385,'d')
 s.rule(449)
 s.text(45,502,'沿槽面法线入射','heading')
 s.text(45,547,'Littrow：α = β = γ','note')
 s.text(45,591,'mλ = 2d sin γ','math')
 s.path([(682,575),(682,487)],dash=True)
 s.path([(651,500),(686,574)],'ray',True)
 s.path([(678,576),(643,502)],'answer',True)
 s.path([(625,591),(732,556)])
 s.text(729,527,'α = β','note')
 s.text(45,665,'沿栅面法线入射','heading')
 s.text(45,710,'α = 0，闪耀方向 β = 2γ','note')
 s.text(45,754,'mλ = d sin 2γ','math')
 s.path([(682,735),(682,637)],dash=True)
 s.path([(686,641),(686,735)],'ray',True)
 s.path([(682,735),(608,641)],'answer',True)
 s.path([(630,752),(737,717)])
 s.text(709,680,'β = 2γ','note')
 s.rule(798)
 labelbox(s,844,['α、β 为相对栅面法线的同侧正角。','原题“衍射角 30°”未明确是否指 γ 或 β；','本图不将 30°直接赋给槽面角。'])
 return s

def filtering():
 s=fig(790,'2026 / 频谱与空间滤波器')
 s.text(40,99,'频谱线的振幅（入射振幅 3）','note')
 base=270;xx=[170,310,450,590,730]
 s.path([(80,base),(835,base)],arrow=True);s.text(845,base+8,'νₓ','math')
 for i,(x,amp,lab) in enumerate(zip(xx,[.5,.5,1,.5,.5],['−1/d','−1/(2d)','0','1/(2d)','1/d'])):
  s.path([(x,base),(x,base-120*amp)],'ray',True)
  s.text(x,base-120*amp-18,str(amp).rstrip('0').rstrip('.'),'note','middle')
  s.text(x,base+38,lab,'note','middle')
 s.text(40,385,'滤波器：保留 0、±1/(2d)，阻挡 ±1/d','note')
 # Solid screen with three transparent rectangular apertures: hatch only opaque areas.
 for l,r in [(90,283),(337,423),(477,563),(617,810)]:
  rect(s,l,430,r-l,125)
  # Clip hatch to each opaque region, no white painted holes.
  cid=f'h{l}';s.parts.append(f'<defs><clipPath id="{cid}"><path d="M{l} 430H{r}V555H{l}Z"/></clipPath></defs>')
  s.parts.append(f'<g clip-path="url(#{cid})">')
  for x in range(l-130,r+130,15):s.path([(x,555),(x+125,430)])
  s.end()
 for x in [310,450,590]:
  s.path([(x,413),(x,575)],'answer',True)
  s.text(x,612,['−1/(2d)','0','1/(2d)'][[310,450,590].index(x)],'note','middle')
 labelbox(s,685,['斜线区域不透光；窗口宽度仅作示意。','三条透过谱线的复振幅保持不变：E = 1 + cos(πx′/d)。'])
 return s

class Model:
 def __init__(self,x0,scale,axis,yscale):self.x0=x0;self.s=scale;self.axis=axis;self.ys=yscale
 def p(self,x,y=0):return (self.x0+self.s*x,self.axis-self.ys*y)
 def ray(self,s,points,cls='ray',dash=False):
  pts=[self.p(*p) for p in points]
  if dash:s.path(pts,cls,dash=True)
  else:arrow(s,pts,cls)
 def point(self,s,x,y,label,dx=0,dy=30,cls=''):dot(s,*self.p(x,y),label,dx,dy,cls)
 def axisline(self,s):s.path([(40,self.axis),(865,self.axis)],dash=True)

def aperture2021(solution):
 s=fig(1040 if solution else 455,'2021 / '+('焦面孔阑：完整作图' if solution else '焦面孔阑题图'))
 def setup(axis):
  m=Model(330,1.15,axis,4);m.axisline(s)
  for x,t in [(0,'L₁'),(240,'L₂')]:lens(s,m.p(x)[0],axis,120,t,False)
  stop(s,m.p(120)[0],axis,40,110,'')
  m.point(s,120,10,'P₁',dx=26,dy=-12);s.text(*m.p(143,-16),'P₂','math')
  s.text(*m.p(50,-22.5),'P = F₂','note','middle')
  return m
 m=setup(245)
 if not solution:
  m.ray(s,[(0,6),(240,14)])
  s.text(40,430,'仅给出轴上光线的镜间段；P 与 F₂ 重合。','note');return s
 # Axial marginal ray: f1=-180, f2=120, d=240; focal/image positions exact.
 m.ray(s,[(-180,6),(0,6),(240,14),(408,0)],'secondary')
 m.ray(s,[(-180,0),(0,6)],'secondary',True)
 m.point(s,-180,0,'F₁′');m.point(s,408,0,'A′',dx=20)
 m.ray(s,[(408,0),(408,10)],'answer');m.point(s,408,10,'B′',dx=25,dy=-10)
 s.text(40,424,'① 反向延长定 F₁′；轴上光线交轴定像面。','note')
 s.rule(462)
 m=setup(720)
 # Off-axis infinity ray: same input slope 5/36, aperture height 10.
 chief=[(-180,-35),(0,-10),(120,0),(240,10),(408,10)]
 upper=[(-180,-29),(0,-4),(120,10),(240,24),(408,10)]
 m.ray(s,chief,'answer');m.ray(s,upper,'secondary')
 m.ray(s,[(408,0),(408,10)],'answer');m.point(s,408,0,'A′',dx=20);m.point(s,408,10,'B′',dx=25,dy=-12)
 labelbox(s,922,['② 绿色主光线穿 P，出射平行光轴。','棕色上边缘光线穿 P₁；两束平行入射光同到 B′。'])
 # Verify actual two-lens paths, not merely endpoints.
 for ps in [chief,upper]:
  p0,p1,pq,p2,pi=ps;u0=(p1[1]-p0[1])/180;u12=(p2[1]-p1[1])/240;uo=(pi[1]-p2[1])/168
  assert abs(u12-(u0-p1[1]/-180))<1e-10
  assert abs(uo-(u12-p2[1]/120))<1e-10
  assert abs(p1[1]+120*u12-pq[1])<1e-10
 AUDIT['2021-aperture']={'f1':-180,'f2':120,'d':240,'q':120,'image_x':408,'image_height':10,'chief_output_slope':0,'rays_checked':2}
 return s

def pupil2025(solution):
 s=fig(1080 if solution else 445,'2025 / '+('虚物与入瞳作图' if solution else '薄透镜与孔径光阑'))
 def setup(axis,ys,focus=True):
  m=Model(270,1.12,axis,ys);m.axisline(s)
  for x,t in [(0,'L₁'),(350,'L₂')]:lens(s,m.p(x)[0],axis,139,t)
  stop(s,m.p(210)[0],axis,25*ys,104,'')
  m.point(s,210,0,'Q',dx=-22,dy=-12)
  m.point(s,210,25,'Q₁',dx=25,dy=-10);m.point(s,210,-25,'Q₂',dx=28,dy=29)
  if focus:
   for x,t in [(-100,'F₁'),(100,'F₁′'),(250,'F₂'),(450,'F₂′')]:m.point(s,x,0,t,dy=34)
  m.ray(s,[(500,0),(500,15)]);m.point(s,500,0,'A′',dx=10);m.point(s,500,15,'B′',dx=15,dy=-17)
  return m
 m=setup(255,2.8 if not solution else 1.65)
 if not solution:
  s.text(40,430,'保留给定焦点、Q₁QQ₂ 与实像 A′B′。','note');return s
 xp=210/(1-210/100);yp=25/(1-210/100)
 for target,cls in [(25,'answer'),(-25,'secondary')]:
  y1=-(target+126)/3.2;u0=(-60-y1)/100;u12=u0-y1/100;y2=y1+350*u12;uo=u12-y2/100
  assert abs(y1+210*u12-target)<1e-10 and abs(y2+150*uo-15)<1e-10
  assert abs(y1+u0*xp-target/(1-210/100))<1e-10
  m.ray(s,[(xp,y1+u0*xp),(0,y1),(210,target),(350,y2),(500,15)],cls)
  m.ray(s,[(0,y1),(100,-60)],cls,True)
 m.ray(s,[(100,0),(100,-60)],'answer',True)
 m.point(s,100,0,'A',dx=20,dy=-15);m.point(s,100,-60,'B',dx=20,dy=30)
 m.point(s,xp,yp,'P₁',dx=0,dy=33);m.point(s,xp,-yp,'P₂',dx=0,dy=-16);m.point(s,xp,0,'P',dx=-20,dy=8)
 labelbox(s,461,['① 实线逐面折射并同到 B′；虚线交于虚物 B。','入瞳编号按共轭对应：Q₁ → P₁（下），Q₂ → P₂（上）。'])
 s.rule(541)
 s.text(40,595,'② 光阑经 L₁ 向物方成像，得到入瞳','heading')
 m=Model(270,1.12,815,2.2);m.axisline(s);lens(s,270,815,112,'L₁')
 m.ray(s,[(210,25),(0,0),(xp,yp)],'answer')
 m.ray(s,[(210,25),(0,25),(xp,yp)],'secondary')
 for x,y,t in [(210,25,'Q₁'),(210,0,'Q'),(xp,yp,'P₁'),(xp,0,'P')]:m.point(s,x,y,t,dy=32 if y<=0 else -17)
 labelbox(s,980,['该布局为虚物；不能预先把 AB 放到 L₁ 左侧。','示意距离用于共轭校验，不是原题新增的毫米数。'])
 AUDIT['2025-pupil']={'f1':100,'f2':100,'d':350,'q':210,'object_x':100,'object_height':-60,'image_x':500,'image_height':15,'entrance_pupil_x':xp,'Q1_conjugate_height':yp,'edge_rays_checked':2}
 return s

def pupil2026(solution):
 s=fig(1390 if solution else 465,'2026 / '+('光阑、入瞳、出瞳与主光线' if solution else '给定成像光线'))
 m=Model(430,.8,265,3.3 if not solution else 2.2);m.axisline(s)
 for x,t in [(0,'L₁'),(240,'L₂')]:lens(s,m.p(x)[0],265,126,t,False)
 for x,y,t in [(-150,0,'A'),(-150,-20,'B'),(415,0,'A′'),(120,0,'Q')]:m.point(s,x,y,t,dy=-16 if t=='A' else 30)
 m.ray(s,[(-150,0),(-150,-20)])
 m.ray(s,[(-150,0),(0,15),(240,21),(415,0)])
 if not solution:
  s.text(40,440,'原题只给 Q 中心；上边缘位置尚未画出。','note');return s
 f1=200;f2=21/(.025+.12);q=120;d=240;hq=18
 xp=q/(1-q/f1);yp=hq/(1-q/f1);xep=d+f2*(d-q)/(d-q-f2);yep=f2/(f2-(d-q))*hq
 # Chief ray from B through Q. Incoming/output lines need only extend through pupils.
 ub=.4*20/180;y1=-20+150*ub;u12=ub-y1/f1;y2=y1+d*u12;uo=u12-y2/f2;yb=y2+175*uo
 assert abs(y1+q*u12)<1e-10
 assert abs(y1+xp*ub)<1e-10 and abs(y2+(xep-d)*uo)<1e-10
 m.ray(s,[(-150,-20),(0,y1),(120,0),(240,y2),(415,yb)],'answer')
 m.point(s,120,hq,'Q₁',dx=30,dy=-15);m.point(s,415,yb,'B′',dx=15,dy=-15)
 m.ray(s,[(415,0),(415,yb)],'answer')
 labelbox(s,452,['① 采用给定光线为上边缘光线的作图约定。','其与 Q 所在垂面的交点为 Q₁；绿色主光线穿 Q。'])
 s.rule(535);s.text(40,584,'② 入瞳：Q、Q₁ 经 L₁ 反向成像','heading')
 m=Model(430,.8,760,2);m.axisline(s);lens(s,430,760,80,'L₁',False)
 # Virtual entrance pupil: extensions to the right of L1.
 m.ray(s,[(q,hq),(0,0)],'answer');m.ray(s,[(0,0),(xp,yp)],'answer',True)
 m.ray(s,[(q,hq),(0,hq)],'secondary');m.ray(s,[(0,hq),(xp,yp)],'secondary',True)
 for x,y,t in [(q,hq,'Q₁'),(q,0,'Q'),(xp,yp,'P′'),(xp,0,'P')]:m.point(s,x,y,t,dx=12,dy=-16 if y else 32)
 s.rule(866);s.text(40,917,'③ 出瞳：Q、Q₁ 经 L₂ 正向成像','heading')
 m=Model(430,.8,1155,1.7);m.axisline(s);lens(s,m.p(d)[0],1155,110,'L₂',False)
 m.ray(s,[(q,hq),(d,0),(380,-21)],'answer')
 m.ray(s,[(xep,yep),(d,0)],'answer',True)
 m.ray(s,[(q,hq),(d,hq),(380,hq-140*hq/f2)],'secondary')
 m.ray(s,[(xep,yep),(d,hq)],'secondary',True)
 for x,y,t in [(q,hq,'Q₁'),(q,0,'Q'),(xep,yep,'P₁′'),(xep,0,'P₁')]:m.point(s,x,y,t,dy=-20 if y else 32)
 labelbox(s,1304,['虚瞳用延长线定位，不能把虚线当实际传播。','若给定线不是边缘线，Q₁ 高度不唯一。'])
 AUDIT['2026-pupil']={'f1':f1,'f2':f2,'d':d,'q':q,'Q1_height':hq,'entrance':[xp,yp],'exit':[xep,yep],'chief_image_height':yb,'chief_passes_Q_P_and_P1':True}
 return s

def crystal(solution):
 s=fig(1080 if solution else 560,'2026 / '+('负单轴晶体：惠更斯作图' if solution else '空气—负晶体界面'))
 O=(600 if solution else 440,275);x0,y0=O
 s.path([(45,y0),(850,y0)])
 s.path([(x0,88),(x0,y0+190)],dash=True)
 arrow(s,[(x0+130,y0-185),O]);s.text(x0+48,y0-139,'θ','math')
 raw(s,f'M {x0} {y0-84} A84 84 0 0 1 {x0+48.2} {y0-68.8}')
 s.text(745,y0-25,'空气','note');s.text(45,y0+43,'晶体','note')
 # Independent optical-axis icon preserves the original down-right direction.
 s.path([(90,y0+135),(205,y0+216)],arrow=True,both=True);s.text(62,y0+116,'光轴','note')
 if not solution:
  s.text(40,532,'依题面指定负单轴模型；不代入实际石英的正负性。','note');return s
 theta=math.radians(35);ang=math.radians(35);no,ne=1.8,1.25
 a=(math.cos(ang),math.sin(ang));b=(-a[1],a[0]);G=[[a[i]*a[j]/no**2+b[i]*b[j]/ne**2 for j in range(2)] for i in range(2)]
 px=-math.sin(theta)
 A=G[1][1];B=2*G[0][1]*px;C=G[0][0]*px*px-1
 py=(-B+math.sqrt(B*B-4*A*C))/(2*A)
 pe=(px,py);Te=tuple(sum(G[i][j]*pe[j] for j in range(2)) for i in range(2))
 po=(px,math.sqrt(no*no-px*px));To=tuple(v/no**2 for v in po);Bpoint=(-1/math.sin(theta),0)
 scale=285
 def pt(p):return (x0+scale*p[0],y0+scale*p[1])
 # Clip lower half-space; surface branches above the interface are not propagated.
 s.parts.append('<defs><clipPath id="medium"><path d="M25 275H875V645H25Z"/></clipPath></defs>')
 s.parts.append('<g clip-path="url(#medium)">')
 s.circle(x0,y0,scale/no)
 pts=[]
 for i in range(361):
  t=math.radians(i);v=tuple(a[k]*math.cos(t)/no+b[k]*math.sin(t)/ne for k in range(2));pts.append(pt(v))
 s.path(pts,'answer');s.end()
 dot(s,*O,'O',dx=21,dy=-16)
 dot(s,*pt(Bpoint),'B',dx=0,dy=-16)
 for v,p,label,cls in [(To,po,'Tₒ','ray'),(Te,pe,'Tₑ','answer')]:
  # Tangent extended through contact; both wavefronts originate at the same B.
  end=(.75,(1-p[0]*.75)/p[1]);s.path([pt(Bpoint),pt(end)],cls)
  s.path([O,pt(v)],cls)
  dot(s,*pt(v),label,dx=20 if label=='Tₒ' else -23,dy=30 if label=='Tₒ' else 39,cls='result' if cls=='answer' else '')
  assert abs(sum(p[i]*v[i] for i in range(2))-1)<1e-10
  assert abs(p[0]*Bpoint[0]-1)<1e-10
 s.text(687,531,'Σₒ','math');s.text(705,610,'Σₑ','math result')
 s.text(40,661,'B 为同一入射波前的后到界面点；两切线共用 B。','note')
 s.rule(699)
 s.text(40,749,'波法线与能流方向','heading')
 for cx,cy,p,v,ordinary in [(220,817,po,To,True),(620,817,pe,Te,False)]:
  def normalized(vec,length):
   n=math.hypot(*vec);return (cx+length*vec[0]/n,cy+length*vec[1]/n)
  endk=normalized(p,110);s.path([(cx,cy),endk],'ray',True)
  if ordinary:s.text(72,975,'kₒ ∥ Sₒ','math')
  else:
   ends=normalized(v,135);s.path([(cx,cy),ends],'answer',True)
   s.text(endk[0]+28,endk[1]+12,'kₑ','math');s.text(ends[0]-48,ends[1]+34,'Sₑ','math result')
  s.circle(cx,cy,2.3,fill=INK)
 labelbox(s,1030,['k 垂直波前切线；S 由次波源指向切点。'])
 AUDIT['negative-crystal']={'illustrative_only':True,'no':no,'ne':ne,'theta_degrees':35,'optic_axis_degrees':35,'G':G,'p_o':po,'p_e':pe,'T_o':To,'T_e':Te,'B':Bpoint,'shared_phase_matching_residual':abs(po[0]-pe[0]),'ordinary_k_parallel_S':abs(po[0]*To[1]-po[1]*To[0]),'extraordinary_cross_k_S':pe[0]*Te[1]-pe[1]*Te[0]}
 return s

MAKERS={
 '2016-cavity-source.svg':cavity,'2016-point-source.svg':point,'2017-qswitch-source.svg':qswitch,
 '2018-homogeneous-gain-options.svg':gain,'blazed-grating-angle-conventions.svg':grating,
 'newton-contact-source.svg':newton,'2020-alternating-slits.svg':slits,'2023-double-hole-options.svg':double_hole,
 '2025-young-source.svg':young,'2026-filter-solution.svg':filtering,
 '2021-aperture-source-v2.svg':lambda:aperture2021(False),'2021-aperture-solution.svg':lambda:aperture2021(True),
 '2025-pupil-source.svg':lambda:pupil2025(False),'2025-pupil-solution.svg':lambda:pupil2025(True),
 '2026-pupil-source.svg':lambda:pupil2026(False),'2026-pupil-solution.svg':lambda:pupil2026(True),
 '2026-negative-crystal-source.svg':lambda:crystal(False),'2026-negative-crystal-solution.svg':lambda:crystal(True),
 'prism-2021-source.svg':lambda:make_2021(False),'prism-2021-axes-roof.svg':lambda:make_2021(True),
 'prism-2025-source.svg':lambda:make_2025(False),'prism-2025-axes-roof.svg':lambda:make_2025(True),
 'prism-2026-source.svg':lambda:make_2026(False),'prism-2026-axes.svg':lambda:make_2026(True),
}

def finish(s):
 # External SVG images follow their embedding element's color-scheme.
 # Separate explicit palette exports also permit reproducible dark-theme QA.
 s.parts.insert(4,'''<style>
 .secondary{stroke:#976333;stroke-width:1.5}
 @media (prefers-color-scheme:dark){
 .line{stroke:#E8DCC3}text{fill:#E8DCC3}.answer{stroke:#9CCBBB}.result,.number{fill:#9CCBBB}
 .secondary{stroke:#DDB587}.caution{fill:#DDB587}
 #arrow path{stroke:#E8DCC3}#answer-arrow path{stroke:#9CCBBB}
 circle[style]{fill:#E8DCC3!important}
 }
 </style>''')


def render_one(path,width,dest,bg=None,dark=False):
 runtime=Path('/tmp/optics-svg-render');runtime.mkdir(exist_ok=True)
 env=os.environ.copy()
 for p in ['config','cache','inkscape']:(runtime/p).mkdir(exist_ok=True)
 env.update(XDG_CONFIG_HOME=str(runtime/'config'),XDG_CACHE_HOME=str(runtime/'cache'),INKSCAPE_PROFILE_DIR=str(runtime/'inkscape'))
 source=path
 if dark:
  source=runtime/path.name
  t=path.read_text().replace('#302D27','#E8DCC3').replace('#346D68','#9CCBBB').replace('#976333','#DDB587')
  source.write_text(t)
 args=['inkscape',str(source),'--export-type=png',f'--export-filename={dest}',f'--export-width={width}',f'--export-background-opacity={1 if bg else 0}']
 if bg:args.append('--export-background='+bg)
 subprocess.run(args,env=env,capture_output=True,check=True)


def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for name,func in MAKERS.items():
  s=func();finish(s);s.save(OUT/name)
  print(name,flush=True)
 (ROOT/'物理校验.json').write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2)+'\n')
 if '--render' in sys.argv:
  # Sequential batches stay light on resources; no external service calls.
  for name in MAKERS:
   p=OUT/name
   for width,suffix in [(1800,''),(350,'-350px')]:render_one(p,width,ROOT/'PNG'/(p.stem+suffix+'.png'))
   for theme,bg in [('warm','#FBF5E9'),('white','#FFFFFF'),('dark','#20221F')]:
    render_one(p,700,ROOT/'检查'/(p.stem+'-'+theme+'.png'),bg,theme=='dark')
   print('rendered',name,flush=True)
if __name__=='__main__':main()
