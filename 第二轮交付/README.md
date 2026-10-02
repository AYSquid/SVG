# 第二轮绘图交付

已按 19 道题、24 个文件完成重绘；26 处引用保持原文件名。全部为本地交付，未推送 GitHub、未修改网站。

[离线总览](总览.html) · [中文核对报告](中文核对报告.md) · [棱镜专报](棱镜核对报告.md) · [替换映射](新旧文件对应.csv)

**先审阅条件图**：2025 棱镜的中间面、2026 棱镜的首块屋脊读法有分支；2026 光阑的边缘光线身份及光栅30°归属有条件说明。缺原图的3题与可选教学图未制作。

## 文件

| SVG（保持原名） | 透明预览 |
|---|---|
| [2016-cavity-source.svg](SVG/2016-cavity-source.svg) | [PNG](PNG/2016-cavity-source.png) |
| [2016-point-source.svg](SVG/2016-point-source.svg) | [PNG](PNG/2016-point-source.png) |
| [2017-qswitch-source.svg](SVG/2017-qswitch-source.svg) | [PNG](PNG/2017-qswitch-source.png) |
| [2018-homogeneous-gain-options.svg](SVG/2018-homogeneous-gain-options.svg) | [PNG](PNG/2018-homogeneous-gain-options.png) |
| [2020-alternating-slits.svg](SVG/2020-alternating-slits.svg) | [PNG](PNG/2020-alternating-slits.png) |
| [2021-aperture-solution.svg](SVG/2021-aperture-solution.svg) | [PNG](PNG/2021-aperture-solution.png) |
| [2021-aperture-source-v2.svg](SVG/2021-aperture-source-v2.svg) | [PNG](PNG/2021-aperture-source-v2.png) |
| [2023-double-hole-options.svg](SVG/2023-double-hole-options.svg) | [PNG](PNG/2023-double-hole-options.png) |
| [2025-pupil-solution.svg](SVG/2025-pupil-solution.svg) | [PNG](PNG/2025-pupil-solution.png) |
| [2025-pupil-source.svg](SVG/2025-pupil-source.svg) | [PNG](PNG/2025-pupil-source.png) |
| [2025-young-source.svg](SVG/2025-young-source.svg) | [PNG](PNG/2025-young-source.png) |
| [2026-filter-solution.svg](SVG/2026-filter-solution.svg) | [PNG](PNG/2026-filter-solution.png) |
| [2026-negative-crystal-solution.svg](SVG/2026-negative-crystal-solution.svg) | [PNG](PNG/2026-negative-crystal-solution.png) |
| [2026-negative-crystal-source.svg](SVG/2026-negative-crystal-source.svg) | [PNG](PNG/2026-negative-crystal-source.png) |
| [2026-pupil-solution.svg](SVG/2026-pupil-solution.svg) | [PNG](PNG/2026-pupil-solution.png) |
| [2026-pupil-source.svg](SVG/2026-pupil-source.svg) | [PNG](PNG/2026-pupil-source.png) |
| [blazed-grating-angle-conventions.svg](SVG/blazed-grating-angle-conventions.svg) | [PNG](PNG/blazed-grating-angle-conventions.png) |
| [newton-contact-source.svg](SVG/newton-contact-source.svg) | [PNG](PNG/newton-contact-source.png) |
| [prism-2021-axes-roof.svg](SVG/prism-2021-axes-roof.svg) | [PNG](PNG/prism-2021-axes-roof.png) |
| [prism-2021-source.svg](SVG/prism-2021-source.svg) | [PNG](PNG/prism-2021-source.png) |
| [prism-2025-axes-roof.svg](SVG/prism-2025-axes-roof.svg) | [PNG](PNG/prism-2025-axes-roof.png) |
| [prism-2025-source.svg](SVG/prism-2025-source.svg) | [PNG](PNG/prism-2025-source.png) |
| [prism-2026-axes.svg](SVG/prism-2026-axes.svg) | [PNG](PNG/prism-2026-axes.png) |
| [prism-2026-source.svg](SVG/prism-2026-source.svg) | [PNG](PNG/prism-2026-source.png) |

## 复现与检查

```bash
python3 第二轮交付/tools/draw_all.py --render
python3 第二轮交付/tools/verify_prisms.py
python3 第二轮交付/tools/verify_all.py
python3 第二轮交付/tools/package_review.py
```

需要 Python 3、Inkscape、Noto Sans CJK SC；资产验证使用 Pillow。357 项资产/光学检查通过，棱镜另有 7 个条件模型、58 次变换、15 个坐标检查点。测试不消除原图歧义。

`PNG/` 为48张透明预览，`检查/` 为72张带底色的主题检查图（非正式替换资产）。`tools/` 为绘图与校验代码。所有示意参数仅供构造，不是原题新增尺寸。
