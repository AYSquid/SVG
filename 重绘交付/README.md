# 棱镜作图交付

每年包含不带答案的 source.svg、带完整光路和坐标分图的 solution.svg、对应透明 PNG（1800px 和 350px）。原始材料保留在仓库根目录的年份文件夹中。

| 年份 | 题图 | 解图 | 预览 |
|---|---|---|---|
| 2021 | [SVG](2021/prism-2021-source.svg) | [SVG](2021/prism-2021-solution.svg) | [PNG](2021/prism-2021-solution.png) |
| 2025 | [SVG](2025/prism-2025-source.svg) | [条件解 SVG](2025/prism-2025-solution.svg) | [PNG](2025/prism-2025-solution.png) |
| 2026 | [SVG](2026/prism-2026-source.svg) | [SVG](2026/prism-2026-solution.svg) | [PNG](2026/prism-2026-solution.png) |

先读 [中文核对报告](中文核对报告.md)：2025 中间棱镜仍需更清楚的面结构证据，不能直接将条件解当作唯一答案。2026 主解与第一棱镜为屋脊的备选读法已明确区分。

- [绘图源代码](tools/draw_prisms.py)
- [逐次矩阵检查代码](tools/verify_optics.py)
- [校验结果](矩阵校验.json)
- [独立初读及修订记录](独立读图记录.md)

复现命令见核对报告。交付目录不修改原照、参考答案或网站。
