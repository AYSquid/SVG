#!/usr/bin/env python3
"""Independent numeric and deliverable checks; does not install dependencies."""
from pathlib import Path
import math, cmath, json, hashlib, csv, xml.etree.ElementTree as ET
from PIL import Image
from draw_all import ROOT, MAKERS

REPO=ROOT.parent
checks=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)

def image_height(y0,object_y,object_x,f1,f2,d,image_x):
 u0=(y0-object_y)/(-object_x)
 u12=u0-y0/f1;y2=y0+d*u12;uo=u12-y2/f2
 return y2+(image_x-d)*uo

def main():
 inputs=REPO/'第二轮材料'
 manifest=json.loads((inputs/'文件校验.json').read_text())
 for e in manifest:
  b=(inputs/e['file']).read_bytes()
  check('original '+e['file'],len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'])
 expected={p.name for p in (inputs/'现有SVG').glob('*.svg')}
 check('24 exact retained filenames',set(MAKERS)==expected and len(expected)==24)
 for name in sorted(expected):
  p=ROOT/'SVG'/name;r=ET.parse(p).getroot()
  check('SVG viewBox '+name,float(r.attrib['viewBox'].split()[2])==900)
  check('no embedded raster '+name,not any(e.tag.endswith('image') for e in r.iter()))
  check('no background rectangle '+name,not any(e.tag.endswith('rect') for e in r.iter()))
  check('stroke scaling '+name,'non-scaling-stroke' in p.read_text())
  for suffix,width in [('',1800),('-350px',350)]:
   im=Image.open(ROOT/'PNG'/(p.stem+suffix+'.png'))
   check('transparent preview '+p.stem+suffix,im.width==width and im.mode=='RGBA' and im.getextrema()[3][0]==0)
  for theme in ['warm','white','dark']:
   im=Image.open(ROOT/'检查'/(p.stem+'-'+theme+'.png'));check('theme render '+p.stem+theme,im.width==700)
 # Independently confirm conjugate behavior using two non-edge rays.
 for y0 in [-20,8]:check('2025 object conjugacy '+str(y0),abs(image_height(y0,-60,100,100,100,350,500)-15)<1e-10)
 for y0 in [-25,5]:check('2026 object conjugacy '+str(y0),abs(image_height(y0,-20,-150,200,21/.145,240,415)-50/3)<1e-10)
 data=json.loads((ROOT/'物理校验.json').read_text())
 c=data['negative-crystal'];G=c['G'];p=c['p_e'];T=c['T_e'];B=c['B']
 check('negative model ne<no',c['ne']<c['no'])
 check('e dispersion',abs(sum(p[i]*G[i][j]*p[j] for i in range(2) for j in range(2))-1)<1e-10)
 check('shared tangent B',abs(sum(p[i]*B[i] for i in range(2))-1)<1e-10)
 check('e tangent point',abs(sum(p[i]*T[i] for i in range(2))-1)<1e-10)
 check('phase matching',abs(c['p_o'][0]-p[0])<1e-12)
 check('o k parallel S',abs(c['ordinary_k_parallel_S'])<1e-12)
 check('e k distinct from S',abs(c['extraordinary_cross_k_S'])>1e-3)
 # Trace a periodic aperture independently as an explicit coherent field sum.
 for beta in [.02,.18,.51,1.17]:
  N=7;explicit=sum(cmath.exp(1j*2*beta*x) for j in range(N) for x in [6*j,6*j+2])
  formula=4*math.cos(2*beta)**2*(math.sin(6*N*beta)/math.sin(6*beta))**2
  check('alternating slit pair factor '+str(beta),abs(abs(explicit)**2-formula)<1e-9)
 for x in [-.7,.13,.9]:
  field=1+.5*cmath.exp(1j*math.pi*x)+.5*cmath.exp(-1j*math.pi*x)
  check('filtered field '+str(x),abs(field-(1+math.cos(math.pi*x)))<1e-12)
 check('cavity A stable',0<1*(1-.8)<1)
 check('cavity B stable',0<(1-.5)**2<1)
 check('cavity C unstable R1<L',.5*(1+1/.8)>1)
 check('cavity D boundary',abs(.5*(1+.5/.5)-1)<1e-12)
 result={'status':'passed','check_count':len(checks),'checks':checks,'limitations':['Tests do not settle ambiguous photographed prism faces.','Theme snapshots use explicit palette exports; browser integration remains a maintainer check.','All unnamed diagram distances are illustrative.']}
 (ROOT/'验证结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(checks),'checks; 24 SVG; 48 transparent previews; 72 theme renders; original material hashes unchanged.')

if __name__=='__main__':main()
