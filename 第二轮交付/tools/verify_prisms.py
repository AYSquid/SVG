#!/usr/bin/env python3
"""Numerical orientation audit, standard library only.
This checks specified geometric branches, NOT their truth in the photograph.
R=page right, U=page up, W=out of page. Basis vectors are columns of B.
The illustrative intermediate angles are not measurements or prism designs.
"""
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parents[1]
I=[[float(i==j) for j in range(3)] for i in range(3)]
W=[0.,0.,1.]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return [x/norm(a) for x in a]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def plus(a,b):return [x+y for x,y in zip(a,b)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def tr(a):return [list(x) for x in zip(*a)]
def det(a):return dot(a[0],cross(a[1],a[2]))
def col(a,j):return [a[i][j] for i in range(3)]
def direction(deg):return [math.cos(math.radians(deg)),math.sin(math.radians(deg)),0.]
def basis(x,z):return tr([direction(x),W[:],direction(z)])
def H(n):return [[I[i][j]-2*n[i]*n[j] for j in range(3)] for i in range(3)]
def close(a,b):return norm(sub(a,b))<1e-9
def clean(v):
    if isinstance(v,float):return 0.0 if abs(v)<1e-12 else round(v,12)
    if isinstance(v,list):return [clean(x) for x in v]
    if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
    return v

class Audit:
    def __init__(self,name,x,z):
        self.name=name;self.B=basis(x,z);self.steps=[];self.checkpoints={};self.count=0
        self.initial_det=round(det(self.B))
        self.assert_basis()
    def assert_basis(self):
        assert max(abs(x-I[i][j]) for i,row in enumerate(mm(tr(self.B),self.B)) for j,x in enumerate(row))<1e-9
        hand=round(det(self.B))
        assert hand==self.initial_det*(-1)**self.count
        assert close(cross(col(self.B,0),col(self.B,1)),[hand*x for x in col(self.B,2)])
    def apply(self,M,label,normal=None,reflection=False):
        before=[r[:] for r in self.B]
        self.B=mm(M,self.B)
        if reflection:self.count+=1
        self.assert_basis()
        self.steps.append(dict(label=label,reflection=reflection,normal=normal,matrix=M,before=before,after=self.B,determinant=round(det(self.B)),cumulative_reflections=self.count))
    def ordinary(self,out,label):
        n=unit(sub(col(self.B,2),direction(out)))
        self.apply(H(n),label,n,True)
        assert close(col(self.B,2),direction(out))
    def roof(self,out,label):
        m=unit(sub(col(self.B,2),direction(out)))
        n1=unit(plus(m,W));n2=unit(sub(m,W))
        assert abs(dot(n1,n2))<1e-9
        # A roof's two mutually perpendicular faces, explicitly applied one by one.
        combined=mm(H(n2),H(n1))
        expected=mm(H(m),H(W))
        assert max(abs(combined[i][j]-expected[i][j]) for i in range(3) for j in range(3))<1e-9
        self.apply(H(n1),label+'/first facet',n1,True)
        self.apply(H(n2),label+'/second facet',n2,True)
        assert close(col(self.B,2),direction(out))
    def refract(self,out,label):
        # Orientation-only transport in the same principal section, NOT Snell-law
        # ray tracing or a statement of magnification/index of refraction.
        k=col(self.B,2);theta=math.radians(out)-math.atan2(k[1],k[0])
        c=math.cos(theta);s=math.sin(theta)
        self.apply([[c,-s,0],[s,c,0],[0,0,1]],label)
        assert close(col(self.B,2),direction(out))
    def checkpoint(self,name,x,y,z,count):
        assert self.count==count,(self.name,name,self.count,count)
        assert close(col(self.B,0),direction(x)),(self.name,name,'x')
        assert close(col(self.B,1),[0,0,y]),(self.name,name,'y')
        assert close(col(self.B,2),direction(z)),(self.name,name,'z')
        self.checkpoints[name]=dict(x=col(self.B,0),y=col(self.B,1),z=col(self.B,2),reflections=count,handedness=round(det(self.B)))
    def real_image(self):
        # Transverse image inversion: B_out=B_in diag(-1,-1,1).
        before=[r[:] for r in self.B]
        self.B=mm(self.B,[[-1,0,0],[0,-1,0],[0,0,1]])
        self.assert_basis()
        self.steps.append(dict(label='real image; right multiplication in local basis',reflection=False,local_matrix=[[-1,0,0],[0,-1,0],[0,0,1]],before=before,after=self.B,cumulative_reflections=self.count))
    def result(self):return dict(name=self.name,checkpoints=self.checkpoints,steps=self.steps)


def main():
    audits=[]
    a=Audit('2021',90,0)
    a.ordinary(90,'R1');a.roof(-45,'R2-3')
    a.checkpoint('a',45,-1,-45,3)
    a.ordinary(45,'R4');a.checkpoint('before lens',-45,-1,45,4)
    a.real_image();a.checkpoint('P',135,1,45,4);audits.append(a)
    for roof in [True,False]:
        for exit_reflection in [False,True]:
            a=Audit(f'2025 central_roof={roof} exit_reflection={exit_reflection}',180,90)
            a.roof(-120,'R1-2');a.ordinary(0,'R3');a.checkpoint('a',90,-1,0,3)
            a.ordinary(120,'middle first ordinary reflection')
            if roof:a.roof(-30,'middle upper roof')
            else:a.ordinary(-30,'middle upper ordinary reflection')
            if exit_reflection:a.ordinary(-10,'hypothetical third reflecting face')
            else:a.refract(-10,'T: orientation transport at exit')
            a.ordinary(25,'last prism bottom ordinary reflection')
            a.refract(0,'last exit, parallel to a')
            x=90 if exit_reflection else -90
            y=1 if roof else -1
            a.checkpoint('b',x,y,0,6+int(roof)+int(exit_reflection));audits.append(a)
    for first_roof in [False,True]:
        a=Audit(f'2026 first_roof={first_roof}',90,0)
        a.ordinary(90,'first prism lower ordinary face')
        if first_roof:a.roof(-45,'first prism hypothetical upper roof')
        else:a.ordinary(-45,'R2: first prism upper ordinary face')
        a.roof(180,'middle right roof');a.ordinary(45,'middle left ordinary face')
        a.checkpoint('a',135,1 if first_roof else -1,45,5+int(first_roof))
        a.ordinary(-70,'last prism top ordinary face');a.roof(180,'last prism right roof');a.ordinary(90,'last prism left ordinary face')
        a.checkpoint('b',0,-1 if first_roof else 1,90,9+int(first_roof));audits.append(a)
    output=dict(convention='world coordinates R=right,U=up,W=out; B columns=x,y,z; angles illustrative, not measured',warning='Algebra verifies conditional models only; it cannot identify a face in the photograph.',branches=[a.result() for a in audits])
    (ROOT/'矩阵校验.json').write_text(json.dumps(clean(output),ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {len(audits)} optical branches; {sum(len(a.steps) for a in audits)} transformations; {sum(len(a.checkpoints) for a in audits)} coordinate checkpoints.')
    for a in audits:
        print(a.name, {k:(v['reflections'],v['handedness']) for k,v in a.checkpoints.items()})

if __name__=='__main__':main()
