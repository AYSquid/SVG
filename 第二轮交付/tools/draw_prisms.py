#!/usr/bin/env python3
"""Editable, transparent SVG diagrams. Geometry manually traced from supplied photos.
Run: python3 重绘交付/tools/draw_prisms.py [--render]
PNG rendering uses Inkscape; no downloaded assets and no edits to supplied files.
"""
from pathlib import Path
from html import escape
import math
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INK = '#302D27'
ACCENT = '#346D68'
CAUTION = '#976333'

class SVG:
    def __init__(self, height, title, desc):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-labelledby="title description">
<title id="title">{escape(title)}</title><desc id="description">{escape(desc)}</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{INK}" stroke-width="1.3"/></marker>
<marker id="answer-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" markerUnits="userSpaceOnUse" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{ACCENT}" stroke-width="1.4"/></marker>
</defs>
<style>
.line {{fill:none;stroke:{INK};stroke-width:1.2;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}}
.ray {{stroke-width:1.5}}
.answer {{stroke:{ACCENT};stroke-width:1.5}}
text {{fill:{INK};font:28px 'Noto Sans CJK SC','Microsoft YaHei',sans-serif}}
.math {{font-family:'DejaVu Sans',sans-serif;font-style:italic;font-size:30px}}
.heading {{font-size:30px;font-weight:600}}
.note {{font-size:25px}}
.number {{font-size:25px;fill:{ACCENT}}}
.result {{fill:{ACCENT}}}
.caution {{fill:{CAUTION}}}
</style>''']
    def path(self, pts, cls='', arrow=False, both=False, dash=False):
        d = 'M' + ' L'.join(f'{x:g},{y:g}' for x,y in pts)
        attrs = ''
        if arrow: attrs += f' marker-end="url(#{"answer-arrow" if "answer" in cls else "arrow"})"'
        if both: attrs += ' marker-start="url(#arrow)"'
        if dash: attrs += ' stroke-dasharray="5 6"'
        self.parts.append(f'<path class="line {cls}" d="{d}"{attrs}/>')
    def text(self,x,y,value,cls='',anchor='start'):
        self.parts.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')
    def circle(self,x,y,r,cls='',fill=None):
        self.parts.append(f'<circle class="line {cls}" cx="{x:g}" cy="{y:g}" r="{r:g}"'+(f' style="fill:{fill};stroke:none"' if fill else '')+'/>')
    def symbol(self,x,y,out=True,answer=False):
        cls = 'answer' if answer else ''
        self.circle(x,y,9,cls)
        if out: self.circle(x,y,2.2,fill=ACCENT if answer else INK)
        else:
            self.path([(x-4,y-4),(x+4,y+4)],cls)
            self.path([(x-4,y+4),(x+4,y-4)],cls)
    def axes(self,cx,cy,xa,za,out=True,answer=False,length=64):
        # Mathematical angles (up is +90 degrees), SVG vertical direction inverted.
        cls='answer' if answer else 'ray'
        for label,angle in [('x',xa),('z',za)]:
            a=math.radians(angle)
            p=(cx+length*math.cos(a),cy-length*math.sin(a))
            self.path([(cx,cy),p],cls,True)
            q=(cx+(length+24)*math.cos(a),cy-(length+24)*math.sin(a)+9)
            self.text(*q,label,'math result' if answer else 'math','middle')
        self.symbol(cx,cy,out,answer)
        self.text(cx-25,cy+34,'y','math result' if answer else 'math','middle')
    def group(self,name): self.parts.append(f'<g id="{name}">')
    def end(self): self.parts.append('</g>')
    def save(self,path):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('\n'.join(self.parts+['</svg>'])+'\n',encoding='utf-8')
    def rule(self,y): self.path([(35,y),(865,y)],dash=True)


def photo_geometry(s, year, solution):
    """Only photo geometry: added labels go in a separate editable group."""
    s.group('original-geometry')
    if year==2021:
        s.path([(235,450),(245,150),(380,100),(475,205),(235,450)])
        s.path([(244,192),(418,142)]) # original paired roof strokes
        s.path([(500,370),(545,280),(625,280),(675,370),(500,370)])
        for p in [[(195,345),(338,345)],[(338,345),(342,114)],[(342,114),(585,370)],[(585,370),(835,145)]]:
            s.path(p,'ray',True)
        # Lens (double arrow) is distinct from the image plane P.
        s.path([(712,176),(784,256)],'ray',True,True)
        s.path([(794,100),(876,190)])
        s.text(465,244,'a','math')
        s.text(866,98,'P','math')
        s.axes(80,345,90,0,length=62)
    elif year==2025:
        # Preserve the bends at the middle prism's exit and the final refracting face.
        s.path([(45,216),(94,132),(195,158),(209,285),(111,285),(45,216)])
        s.path([(78,162),(198,193)])
        s.path([(257,260),(291,144),(438,82),(550,118),(257,260)])
        s.path([(280,192),(480,96)])
        s.path([(510,235),(585,152),(683,139),(760,211),(510,235)])
        for p in [[(140,345),(140,144)],[(140,144),(80,251)],[(80,251),(344,218)],[(344,218),(314,134)],[(314,134),(411,185)],[(411,185),(625,225)],[(625,225),(729,182)],[(729,182),(859,166)]]:
            s.path(p,'ray',True)
        s.text(225,204,'a','math')
        s.text(802,143,'b','math')
    else:
        # First prism: one upper edge; no invented second full roof stroke.
        s.path([(248,315),(263,161),(343,125),(420,156),(248,315)])
        # Do not turn a faint/overlapping upper edge into a new roof strip.
        s.path([(380,327),(470,268),(575,374),(438,542),(380,327)])
        s.path([(433,520),(558,357)])
        s.path([(548,130),(658,266),(758,135),(548,130)])
        s.path([(644,249),(739,135)])
        for p in [[(209,242),(326,242)],[(326,242),(321,135)],[(321,135),(535,423)],[(535,423),(398,414)],[(398,414),(670,133)],[(670,133),(704,206)],[(704,206),(620,219)],[(620,219),(675,52)]]:
            s.path(p,'ray',True)
        s.text(568,305,'a','math')
        s.text(704,67,'b','math')
        s.axes(90,242,90,0,length=59)
    s.end()
    if not solution:return
    s.group('reflection-labels')
    if year==2021:
        for x,y,t in [(279,382,'R1'),(355,77,'R2–3'),(558,414,'R4')]:s.text(x,y,t,'number')
        s.text(732,294,'物镜','note')
    elif year==2025:
        for x,y,t in [(95,111,'R1–2'),(38,307,'R3'),(317,256,'R4'),(352,119,'R5–6*'),(606,269,'R7*')]:s.text(x,y,t,'number')
        s.text(412,219,'T*','number')
    else:
        for x,y,t in [(272,277,'R1'),(343,106,'R2'),(557,446,'R3–4'),(335,441,'R5'),(584,103,'R6'),(718,247,'R7–8'),(566,209,'R9')]:s.text(x,y,t,'number')
    s.end()


def make_2021(solution):
    s=SVG(930 if solution else 515,'2021 棱镜—物镜系统'+('：坐标解图' if solution else '：题图'),
          '保留入射坐标、a、物镜和像面 P；第一棱镜上部双线按屋脊。'+('a 为右上、纸内、右下；P 为左上、纸外、右上。' if solution else '不含待求坐标。'))
    s.text(35,44,'2021  /  '+('坐标与成像' if solution else '题图'),'heading')
    photo_geometry(s,2021,solution)
    s.text(35,496,'P 为题干指定的像方焦面、成像位置。','note')
    if solution:
        s.rule(528)
        s.text(65,580,'a  ·  3 次反射','heading result')
        s.text(490,580,'P  ·  实像横向反号','heading result')
        s.axes(230,704,45,-45,False,True,72)
        s.axes(662,704,135,45,True,True,72)
        s.text(64,831,'透镜前：x 右下、y 纸内；成实像后两者反向。','note')
        s.text(64,882,'⊙ 纸外    ⊗ 纸内    z 沿光传播方向','note')
    return s


def make_2025(solution):
    s=SVG(1240 if solution else 433,'2025 三棱镜系统'+('：条件解图' if solution else '：题图'),
          '原题无入射坐标轴。'+('自选 x 左、y 纸外、z 上。中间双线按屋脊且 T 为出射折射时，a 上内右，b 下外右；其他读法见核对报告。' if solution else '保留光路及 a、b 标签，不添加入射坐标。'))
    s.text(35,44,'2025  /  '+('条件解图' if solution else '题图'),'heading')
    photo_geometry(s,2025,solution)
    s.text(35,399,'原题未给入射坐标轴。','note')
    if solution:
        s.rule(426)
        s.text(40,475,'自选入射：x ←，y ⊙，z ↑','heading result')
        s.text(40,520,'* 主图编号条件：中间双线为屋脊，T 为折射。','note caution')
        s.text(65,584,'a  ·  3 次反射','heading result')
        s.text(500,584,'b  ·  7 次反射*','heading result')
        s.axes(220,708,90,0,False,True,68)
        s.axes(652,708,-90,0,True,True,68)
        s.text(55,862,'该条件下：x_b = −x_a，y_b = −y_a，z_b = z_a。','note result')
        s.rule(894)
        s.text(40,943,'另一读法：中间为 3 次普通反射','heading caution')
        s.text(40,990,'若细线是透视边，并另有第 3 个反射面：','note')
        s.text(40,1035,'b 与 a 同向，即 x ↑、y ⊗、z →。','note')
        s.text(40,1094,'照片不足以唯一确定中间面的三维结构。','note caution')
        s.text(40,1140,'不能仅凭反射次数相同，认定坐标相同。','note')
        s.text(40,1194,'其余条件组合、所缺证据见中文核对报告。','note')
    return s


def make_2026(solution):
    s=SVG(1215 if solution else 630,'2026 三棱镜系统'+('：坐标解图' if solution else '：题图'),
          '两条斜光线在中间棱镜内部直接相交，不在交点反射。'+('第一棱镜按两个普通反射面读图；a 左上、纸内、右上，b 右、纸外、上。' if solution else '保留入射坐标和 a、b。'))
    s.text(35,44,'2026  /  '+('坐标与反射顺序' if solution else '题图'),'heading')
    photo_geometry(s,2026,solution)
    s.text(35,602,'中间光线相交处没有反射面。','note')
    if solution:
        s.rule(638)
        s.text(55,692,'a  ·  5 次反射','heading result')
        s.text(480,692,'b  ·  9 次反射','heading result')
        s.axes(225,820,135,45,False,True,70)
        s.axes(645,820,0,90,True,True,70)
        s.text(45,954,'主解：第一棱镜为 2 次普通反射。','note')
        s.text(45,1000,'后两块棱镜的成对斜线按屋脊处理。','note')
        s.rule(1034)
        s.text(45,1082,'若补充证据确认第一块顶部也是屋脊：','note caution')
        s.text(45,1128,'x、z 不变；a 的 y 改为 ⊙，b 的 y 改为 ⊗。','note')
        s.text(45,1174,'该分支累计反射为 6 / 10 次，详见报告。','note')
    return s


def render(path, width, suffix):
    env=os.environ.copy()
    # Profiles/caches stay outside the checkout. Never override HOME.
    runtime=Path('/tmp/prism-svg-render')
    for name in ['config','cache','inkscape']:(runtime/name).mkdir(parents=True,exist_ok=True)
    env.update(XDG_CONFIG_HOME=str(runtime/'config'),XDG_CACHE_HOME=str(runtime/'cache'),INKSCAPE_PROFILE_DIR=str(runtime/'inkscape'))
    out=path.with_name(path.stem+suffix+'.png')
    subprocess.run(['inkscape',str(path),'--export-type=png',f'--export-filename={out}',f'--export-width={width}','--export-background-opacity=0'],env=env,check=True,capture_output=True)


def main():
    for year,func in [(2021,make_2021),(2025,make_2025),(2026,make_2026)]:
        for solution in [False,True]:
            path=ROOT/str(year)/f'prism-{year}-{"solution" if solution else "source"}.svg'
            func(solution).save(path)
            if '--render' in sys.argv:
                render(path,1800,'')
                render(path,350,'-350px')
            print(path.relative_to(ROOT))

if __name__=='__main__':main()
