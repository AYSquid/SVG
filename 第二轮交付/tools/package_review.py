#!/usr/bin/env python3
"""Build local review index, exact replacement mapping, checksums, and ZIP."""
from pathlib import Path
import csv, json, hashlib, zipfile
from html import escape
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent

def main():
 with (REPO/'第二轮材料/绘图文件清单.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 assert len(rows)==26
 names=sorted({r['文件名'] for r in rows});assert len(names)==24
 with (ROOT/'新旧文件对应.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['题目ID','年份','题号','用途','旧网站路径','新交付文件','状态']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in rows:
   name=r['文件名'];state='条件图：先读核对报告' if name in ['prism-2025-axes-roof.svg','prism-2026-axes.svg','2026-pupil-solution.svg','blazed-grating-angle-conventions.svg'] else '已重绘并检查'
   w.writerow(dict(题目ID=r['题目ID'],年份=r['年份'],题号=r['题号'],用途=r['用途'],旧网站路径=r['网站路径'],新交付文件='SVG/'+name,状态=state))
 html=['''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>24 张配图重绘交付</title>
<style>
:root{color-scheme:light}body{margin:0;background:#FBF5E9;color:#302D27;font:16px/1.7 system-ui,'Noto Sans CJK SC',sans-serif}main{max-width:1060px;margin:auto;padding:28px}h1{font-size:28px}h2{font-size:19px;overflow-wrap:anywhere}a{color:inherit}header{padding-bottom:24px}nav{display:flex;flex-wrap:wrap;gap:12px;align-items:center}select,input{font:inherit;padding:7px;border:1px solid #aaa;background:transparent;color:inherit}article{padding:24px 0;border-top:1px solid #aaa}img{display:block;width:min(100%,700px);height:auto;margin:18px auto}body.mobile img{width:min(100%,350px)}small{display:block;overflow-wrap:anywhere}.note{border-left:3px solid #976333;padding-left:16px}body.dark{background:#20221F;color:#E8DCC3}body.white{background:white}button{font:inherit}article[hidden]{display:none}
</style></head><body><main><header><h1>19 道题 · 24 张配图</h1><p>保留网站文件名；题图、选项图与解图分开。这里展示三种主题的检查图，点击 SVG 可查看可编辑原件。</p><p class="note">2025 棱镜、2026 棱镜、2026 光阑与闪耀光栅含条件说明，接入前请先读核对报告。</p><p><a href="中文核对报告.md">核对报告</a> · <a href="棱镜核对报告.md">棱镜专报</a> · <a href="新旧文件对应.csv">26 处引用映射</a></p>
<nav><label>主题 <select id="theme"><option value="warm">暖米白</option><option value="white">白底</option><option value="dark">深色</option></select></label><label>宽度 <select id="width"><option value="700">700 px</option><option value="350">350 px</option></select></label><label>查找 <input id="query" placeholder="年份或文件名"></label></nav></header>''']
 readme=['# 第二轮绘图交付','', '已按 19 道题、24 个文件完成重绘；26 处引用保持原文件名。全部为本地交付，未推送 GitHub、未修改网站。','', '[离线总览](总览.html) · [中文核对报告](中文核对报告.md) · [棱镜专报](棱镜核对报告.md) · [替换映射](新旧文件对应.csv)','', '**先审阅条件图**：2025 棱镜的中间面、2026 棱镜的首块屋脊读法有分支；2026 光阑的边缘光线身份及光栅30°归属有条件说明。缺原图的3题与可选教学图未制作。','', '## 文件','', '| SVG（保持原名） | 透明预览 |','|---|---|']
 for name in names:
  stem=Path(name).stem;refs=[r for r in rows if r['文件名']==name]
  label='；'.join(f"{r['年份']} · {r['题号']} · {r['用途']}" for r in refs)
  html.append(f'<article data-name="{escape(name)}"><h2>{escape(name)}</h2><small>{escape(label)}</small><p><a href="SVG/{name}">SVG</a> · <a href="PNG/{stem}.png">1800px 透明 PNG</a> · <a href="PNG/{stem}-350px.png">350px 透明 PNG</a></p><img loading="lazy" data-stem="{stem}" src="检查/{stem}-warm.png" alt="{escape(name)}"></article>')
  readme.append(f'| [{name}](SVG/{name}) | [PNG](PNG/{stem}.png) |')
 html.append('''<script>
const theme=document.getElementById('theme'),width=document.getElementById('width'),query=document.getElementById('query');
function update(){document.body.className=(theme.value==='warm'?'':theme.value)+(width.value==='350'?' mobile':'');document.documentElement.style.colorScheme=theme.value==='dark'?'dark':'light';document.querySelectorAll('img[data-stem]').forEach(img=>img.src='检查/'+img.dataset.stem+'-'+theme.value+'.png');document.querySelectorAll('article').forEach(el=>el.hidden=!el.dataset.name.toLowerCase().includes(query.value.toLowerCase()));}
theme.addEventListener('change',update);width.addEventListener('change',update);query.addEventListener('input',update);
</script></main></body></html>''')
 (ROOT/'总览.html').write_text('\n'.join(html))
 readme.extend(['','## 复现与检查','','```bash','python3 第二轮交付/tools/draw_all.py --render','python3 第二轮交付/tools/verify_prisms.py','python3 第二轮交付/tools/verify_all.py','python3 第二轮交付/tools/package_review.py','```','','需要 Python 3、Inkscape、Noto Sans CJK SC；资产验证使用 Pillow。357 项资产/光学检查通过，棱镜另有 7 个条件模型、58 次变换、15 个坐标检查点。测试不消除原图歧义。','','`PNG/` 为48张透明预览，`检查/` 为72张带底色的主题检查图（非正式替换资产）。`tools/` 为绘图与校验代码。所有示意参数仅供构造，不是原题新增尺寸。'])
 (ROOT/'README.md').write_text('\n'.join(readme)+'\n')
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='交付校验.json')
 manifest=[dict(file=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
 (ROOT/'交付校验.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 archive=REPO/'第二轮绘图交付.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files+[ROOT/'交付校验.json']:z.write(p,p.relative_to(REPO))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 print(f'Packaged {len(files)+1} files; 24 SVG, 26 reference mappings; ZIP {archive.stat().st_size} bytes.')
if __name__=='__main__':main()
