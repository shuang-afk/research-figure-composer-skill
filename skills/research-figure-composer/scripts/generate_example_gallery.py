#!/usr/bin/env python3
"""Generate reusable SVG examples for the research figure intake gallery."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "examples"
FONT = "Arial, Microsoft YaHei, Noto Sans CJK SC, sans-serif"
PALETTES = [
    ("nmi-pastel", "NMI低饱和", ["#484878", "#7884B4", "#B4C0E4", "#E4CCD8"]),
    ("semantic", "语义对比", ["#0F4D92", "#8BCF8B", "#B64342", "#42949E"]),
    ("material", "材料机制", ["#33B5A5", "#77D7D1", "#7C6CCF", "#B9A7E8"]),
    ("clinical", "临床随访", ["#272727", "#E28E2C", "#D24B40", "#5B8FD6"]),
    ("genomics", "组学系统", ["#4D4D4D", "#8F8F8F", "#D9544D", "#5B7FCA"]),
]


def t(x, y, value, size=12, weight="400", anchor="middle", fill="#202124"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>'
    )


def r(x, y, w, h, fill="#fff", stroke="#202124", sw=1.1, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, color="#202124", sw=1.2, arrow=True, dash=False):
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    dashed = ' stroke-dasharray="4 3"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{dashed}{marker}/>'


def svg_wrap(title, body, w=520, h=330):
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            "<defs>",
            '<marker id="arrow" viewBox="0 0 10 10" refX="8.4" refY="5" markerWidth="6" markerHeight="6" orient="auto">',
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#202124"/>',
            "</marker>",
            "</defs>",
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            t(26, 34, title, size=18, weight="700", anchor="start"),
            body,
            "</svg>",
        ]
    )


def example_bar():
    colors = ["#484878", "#7884B4", "#B4C0E4", "#E4CCD8", "#F0C0CC"]
    values = [0.68, 0.74, 0.80, 0.86, 0.91]
    parts = [line(76, 254, 456, 254, arrow=False), line(76, 74, 76, 254, arrow=False)]
    for i, v in enumerate(values):
        x = 105 + i * 70
        h = int(v * 168)
        parts.append(r(x, 254 - h, 38, h, colors[i], sw=0.8))
        parts.append(t(x + 19, 274, ["A", "B", "C", "D", "E"][i], size=12))
    parts.append(t(266, 310, "bar / nmi-pastel / SVG text", size=12, fill="#5f6368"))
    return svg_wrap("柱状图示例", "\n".join(parts))


def example_line():
    colors = ["#272727", "#E28E2C", "#D24B40", "#5B8FD6"]
    ys = [[230, 210, 190, 172], [230, 195, 165, 130], [230, 185, 148, 100], [230, 205, 178, 145]]
    xs = [95, 190, 285, 380]
    parts = [line(76, 254, 456, 254, arrow=False), line(76, 74, 76, 254, arrow=False)]
    for idx, series in enumerate(ys):
        pts = " ".join(f"{x},{y}" for x, y in zip(xs, series))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{colors[idx]}" stroke-width="2"/>')
        for x, y in zip(xs, series):
            parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{colors[idx]}" stroke="white" stroke-width="0.7"/>')
    parts.append(t(266, 310, "trend / clinical / shared axes", size=12, fill="#5f6368"))
    return svg_wrap("趋势图示例", "\n".join(parts))


def example_heatmap():
    colors = ["#f7fbff", "#deebf7", "#9ecae1", "#4292c6", "#084594"]
    parts = []
    for row in range(4):
        for col in range(6):
            parts.append(r(98 + col * 52, 82 + row * 42, 46, 34, colors[(row + col) % len(colors)], stroke="#ffffff", sw=1))
    parts.append(t(266, 285, "heatmap / genomics / compact labels", size=12, fill="#5f6368"))
    return svg_wrap("热图示例", "\n".join(parts))


def example_mechanism():
    colors = ["#33B5A5", "#77D7D1", "#7C6CCF", "#B9A7E8", "#E53935"]
    labels = ["刺激", "受体", "信号轴", "效应器", "表型"]
    parts = []
    for i, label in enumerate(labels):
        x = 45 + i * 91
        parts.append(r(x, 138, 68, 54, colors[i], stroke=colors[i], sw=1.3, rx=8))
        parts.append(t(x + 34, 171, label, size=13, weight="700"))
        if i < len(labels) - 1:
            parts.append(line(x + 68, 165, x + 91, 165))
    parts.append(t(266, 258, "mechanism / material / pale nodes", size=12, fill="#5f6368"))
    return svg_wrap("机制图示例", "\n".join(parts))


def example_workflow():
    colors = ["#ffffff", "#f8f9fa", "#ffffff", "#f8f9fa"]
    labels = ["问题", "设计", "分析", "发表"]
    parts = []
    for i, label in enumerate(labels):
        x = 70 + i * 105
        parts.append(r(x, 132, 76, 52, colors[i], stroke="#202124", sw=1.3, rx=0))
        parts.append(t(x + 38, 164, label, size=14, weight="700"))
        if i < len(labels) - 1:
            parts.append(line(x + 76, 158, x + 105, 158))
    parts.append(line(340, 184, 190, 232, color="#2166ac", dash=True))
    parts.append(t(266, 286, "workflow / Nature line art / feedback loop", size=12, fill="#5f6368"))
    return svg_wrap("流程图示例", "\n".join(parts))


def example_architecture():
    colors = ["#484878", "#7884B4", "#E4CCD8", "#F0C0CC"]
    parts = [
        r(55, 102, 88, 48, colors[0], stroke=colors[0], rx=8),
        r(55, 190, 88, 48, colors[1], stroke=colors[1], rx=8),
        r(205, 145, 96, 54, colors[2], stroke=colors[2], rx=8),
        r(365, 145, 98, 54, colors[3], stroke=colors[3], rx=8),
        t(99, 132, "图像", size=13, weight="700"),
        t(99, 220, "文本", size=13, weight="700"),
        t(253, 177, "融合层", size=13, weight="700"),
        t(414, 177, "预测", size=13, weight="700"),
        line(143, 126, 205, 162),
        line(143, 214, 205, 183),
        line(301, 172, 365, 172),
        t(266, 285, "model architecture / nmi-pastel / multimodal", size=12, fill="#5f6368"),
    ]
    return svg_wrap("模型架构示例", "\n".join(parts))


def palette_data_comparison():
    panel_w, panel_h = 260, 158
    gap = 22
    margin_x, margin_y = 28, 62
    w = margin_x * 2 + panel_w * 3 + gap * 2
    h = margin_y + panel_h * 2 + gap + 34
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        t(28, 34, "数据图色系对比", size=18, weight="700", anchor="start"),
        t(28, 56, "同一组折线数据，仅替换色系", size=12, fill="#5f6368", anchor="start"),
    ]
    xs = [0, 48, 96, 144]
    series = [[94, 82, 70, 58], [94, 72, 55, 38], [94, 86, 76, 62]]
    for idx, (name, label, colors) in enumerate(PALETTES):
        row, col = divmod(idx, 3)
        x0 = margin_x + col * (panel_w + gap)
        y0 = margin_y + row * (panel_h + gap)
        parts.append(r(x0, y0, panel_w, panel_h, "#ffffff", stroke="#d6d9dd", sw=1))
        parts.append(t(x0 + 13, y0 + 22, name, size=13, weight="700", anchor="start"))
        parts.append(t(x0 + 13, y0 + 40, label, size=10, fill="#5f6368", anchor="start"))
        parts.append(line(x0 + 36, y0 + 126, x0 + 222, y0 + 126, arrow=False, sw=1))
        parts.append(line(x0 + 36, y0 + 42, x0 + 36, y0 + 126, arrow=False, sw=1))
        for s_idx, ys in enumerate(series):
            pts = " ".join(f"{x0 + 48 + x},{y0 + y}" for x, y in zip(xs, ys))
            color = colors[s_idx % len(colors)]
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/>')
            for x, y in zip(xs, ys):
                parts.append(f'<circle cx="{x0 + 48 + x}" cy="{y0 + y}" r="3.2" fill="{color}" stroke="white" stroke-width="0.6"/>')
        for sw_idx, color in enumerate(colors):
            parts.append(r(x0 + 176 + sw_idx * 14, y0 + 18, 10, 10, color, stroke="#ffffff", sw=0.5, rx=2))
    parts.append("</svg>")
    return "\n".join(parts)


def palette_diagram_comparison():
    panel_w, panel_h = 260, 158
    gap = 22
    margin_x, margin_y = 28, 62
    w = margin_x * 2 + panel_w * 3 + gap * 2
    h = margin_y + panel_h * 2 + gap + 34
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="8.4" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">',
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#202124"/>',
        "</marker>",
        "</defs>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        t(28, 34, "示意图色系对比", size=18, weight="700", anchor="start"),
        t(28, 56, "同一套节点结构，仅替换色系", size=12, fill="#5f6368", anchor="start"),
    ]
    node_labels = ["输入", "编码", "融合", "输出"]
    for idx, (name, label, colors) in enumerate(PALETTES):
        row, col = divmod(idx, 3)
        x0 = margin_x + col * (panel_w + gap)
        y0 = margin_y + row * (panel_h + gap)
        parts.append(r(x0, y0, panel_w, panel_h, "#ffffff", stroke="#d6d9dd", sw=1))
        parts.append(t(x0 + 13, y0 + 22, name, size=13, weight="700", anchor="start"))
        parts.append(t(x0 + 13, y0 + 40, label, size=10, fill="#5f6368", anchor="start"))
        for n_idx, node_label in enumerate(node_labels):
            nx = x0 + 20 + n_idx * 58
            ny = y0 + 79
            color = colors[n_idx % len(colors)]
            parts.append(r(nx, ny, 45, 34, color, stroke=color, sw=1.1, rx=6))
            parts.append(t(nx + 22.5, ny + 22, node_label, size=10, weight="700"))
            if n_idx < len(node_labels) - 1:
                parts.append(line(nx + 45, ny + 17, nx + 58, ny + 17, sw=1.1))
        for sw_idx, color in enumerate(colors):
            parts.append(r(x0 + 176 + sw_idx * 14, y0 + 18, 10, 10, color, stroke="#ffffff", sw=0.5, rx=2))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    examples = {
        "bar.svg": example_bar(),
        "line.svg": example_line(),
        "heatmap.svg": example_heatmap(),
        "mechanism.svg": example_mechanism(),
        "workflow.svg": example_workflow(),
        "model-architecture.svg": example_architecture(),
        "palette-data.svg": palette_data_comparison(),
        "palette-diagram.svg": palette_diagram_comparison(),
    }
    for name, content in examples.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote {OUT / name}")


if __name__ == "__main__":
    main()
