#!/usr/bin/env python3
"""Generate editable SVG data figures with conservative journal styling."""

from __future__ import annotations

import argparse
import csv
import html
import importlib
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


PLOT_DEPENDENCIES = (
    ("matplotlib.pyplot", "matplotlib"),
    ("numpy", "numpy"),
)

PALETTES = {
    "semantic": [
        "#0F4D92",
        "#8BCF8B",
        "#B64342",
        "#42949E",
        "#9A4D8E",
        "#CFCECE",
        "#767676",
        "#272727",
    ],
    "nmi-pastel": [
        "#484878",
        "#7884B4",
        "#B4C0E4",
        "#E4E4F0",
        "#E4CCD8",
        "#F0C0CC",
        "#606060",
    ],
    "material": [
        "#33B5A5",
        "#77D7D1",
        "#7C6CCF",
        "#B9A7E8",
        "#D9D9D9",
        "#E53935",
    ],
    "clinical": [
        "#272727",
        "#E28E2C",
        "#D24B40",
        "#5B8FD6",
        "#7BAA5B",
        "#C45AD6",
    ],
    "genomics": [
        "#4D4D4D",
        "#8F8F8F",
        "#D9544D",
        "#5B7FCA",
        "#B89BD9",
        "#D8D8D8",
    ],
}


def palette_colors(name: str, count: int) -> list[str]:
    colors = PALETTES[name]
    return [colors[index % len(colors)] for index in range(count)]


def module_importable(name: str) -> bool:
    try:
        importlib.import_module(name)
    except Exception:
        return False
    return True


def purge_import_cache(top_level_names: tuple[str, ...]) -> None:
    for name in list(sys.modules):
        if any(name == top or name.startswith(f"{top}.") for top in top_level_names):
            del sys.modules[name]


def install_plot_dependencies() -> bool:
    missing = [package for module_name, package in PLOT_DEPENDENCIES if not module_importable(module_name)]
    if not missing:
        return True

    purge_import_cache(("matplotlib", "numpy"))
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--upgrade",
        "matplotlib",
        "numpy",
    ]
    print(f"installing missing plotting dependencies: {', '.join(missing)}", file=sys.stderr)
    print(" ".join(cmd), file=sys.stderr)
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except OSError as exc:
        print(f"dependency installation failed: {exc}", file=sys.stderr)
        return False
    if result.returncode != 0:
        tail = "\n".join((result.stdout + "\n" + result.stderr).splitlines()[-20:])
        print(f"dependency installation failed with exit code {result.returncode}", file=sys.stderr)
        if tail:
            print(tail, file=sys.stderr)
        return False
    print("plotting dependencies installed", file=sys.stderr)
    importlib.invalidate_caches()
    purge_import_cache(("matplotlib", "numpy"))
    return all(module_importable(module_name) for module_name, _ in PLOT_DEPENDENCIES)


def import_matplotlib(auto_install: bool):
    if auto_install and not install_plot_dependencies():
        return None

    try:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    mpl.rcParams.update(
        {
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
            "font.size": 7,
            "axes.labelsize": 7,
            "axes.titlesize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 6,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.transparent": False,
        }
    )
    return plt


def read_rows(path: Path) -> list[dict[str, str]]:
    sample = path.read_text(encoding="utf-8-sig").splitlines()
    if not sample:
        raise SystemExit(f"Input file is empty: {path}")
    delimiter = "\t" if path.suffix.lower() in {".tsv", ".tab"} else ","
    reader = csv.DictReader(sample, delimiter=delimiter)
    rows = list(reader)
    if not reader.fieldnames:
        raise SystemExit("Input file needs a header row.")
    return rows


def to_float(value: str, label: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise SystemExit(f"Column {label!r} contains non-numeric value {value!r}.") from exc


def grouped(rows: list[dict[str, str]], group_key: str | None) -> dict[str, list[dict[str, str]]]:
    if not group_key:
        return {"": rows}
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[row.get(group_key, "")].append(row)
    return dict(out)


def plot_line_or_scatter(ax, rows, x_key, y_key, group_key, kind, colors):
    for index, (name, group_rows) in enumerate(grouped(rows, group_key).items()):
        xs = [to_float(row[x_key], x_key) for row in group_rows]
        ys = [to_float(row[y_key], y_key) for row in group_rows]
        pairs = sorted(zip(xs, ys), key=lambda item: item[0])
        xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
        color = colors[index % len(colors)]
        label = name if name else None
        if kind == "line":
            ax.plot(xs, ys, marker="o", markersize=3.2, linewidth=1.2, color=color, label=label)
        else:
            ax.scatter(xs, ys, s=18, color=color, label=label, edgecolor="white", linewidth=0.35)


def plot_bar(ax, rows, x_key, y_key, group_key, colors):
    if group_key:
        groups = grouped(rows, group_key)
        categories = list(dict.fromkeys(row[x_key] for row in rows))
        width = 0.8 / max(len(groups), 1)
        offsets = [i - (len(groups) - 1) / 2 for i in range(len(groups))]
        for idx, ((name, group_rows), offset) in enumerate(zip(groups.items(), offsets)):
            values_by_category = {row[x_key]: to_float(row[y_key], y_key) for row in group_rows}
            xs = [i + offset * width for i in range(len(categories))]
            ys = [values_by_category.get(category, math.nan) for category in categories]
            ax.bar(xs, ys, width=width, label=name, color=colors[idx % len(colors)], edgecolor="black", linewidth=0.45)
        ax.set_xticks(range(len(categories)), categories)
    else:
        categories = [row[x_key] for row in rows]
        values = [to_float(row[y_key], y_key) for row in rows]
        ax.bar(range(len(categories)), values, color=colors[: len(categories)], edgecolor="black", linewidth=0.45)
        ax.set_xticks(range(len(categories)), categories)


def plot_box(ax, rows, x_key, y_key, group_key, colors):
    key = group_key or x_key
    groups = grouped(rows, key)
    labels = list(groups.keys())
    values = [[to_float(row[y_key], y_key) for row in group_rows] for group_rows in groups.values()]
    box = ax.boxplot(values, labels=labels, patch_artist=True, widths=0.55, showfliers=False)
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor("black")
        patch.set_linewidth(0.7)
    for part in ("whiskers", "caps", "medians"):
        for artist in box[part]:
            artist.set_color("black")
            artist.set_linewidth(0.8)


def plot_heatmap(ax, rows, x_key, y_key, value_key):
    import numpy as np

    xs = list(dict.fromkeys(row[x_key] for row in rows))
    ys = list(dict.fromkeys(row[y_key] for row in rows))
    grid = np.full((len(ys), len(xs)), np.nan)
    for row in rows:
        grid[ys.index(row[y_key]), xs.index(row[x_key])] = to_float(row[value_key], value_key)
    image = ax.imshow(grid, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(xs)), xs)
    ax.set_yticks(range(len(ys)), ys)
    return image


def _scale(value: float, data_min: float, data_max: float, out_min: float, out_max: float) -> float:
    if data_max == data_min:
        return (out_min + out_max) / 2
    return out_min + (value - data_min) * (out_max - out_min) / (data_max - data_min)


def _svg_text(x, y, text, size=12, anchor="middle", weight="normal", rotate=None):
    transform = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate else ""
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{transform}>'
        f"{html.escape(str(text))}</text>"
    )


def save_basic_svg(rows, args) -> None:
    if args.kind not in {"line", "scatter", "bar"}:
        raise SystemExit(
            f"{args.kind} requires matplotlib/numpy. Install with: python -m pip install matplotlib numpy"
        )

    width = int(args.width * 100)
    height = int(args.height * 100)
    left, right, top, bottom = 58, 20, 34, 52
    plot_w = width - left - right
    plot_h = height - top - bottom
    palette = palette_colors(args.palette, 12)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="black" stroke-width="1"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="black" stroke-width="1"/>',
    ]
    if args.title:
        parts.append(_svg_text(width / 2, 18, args.title, size=12, weight="bold"))

    if args.kind in {"line", "scatter"}:
        groups = grouped(rows, args.group)
        xs_all = [to_float(row[args.x], args.x) for row in rows]
        ys_all = [to_float(row[args.y], args.y) for row in rows]
        x_min, x_max = min(xs_all), max(xs_all)
        y_min, y_max = min(ys_all), max(ys_all)
        y_pad = (y_max - y_min) * 0.08 or 1
        y_min -= y_pad
        y_max += y_pad

        for tick in range(5):
            frac = tick / 4
            x = left + frac * plot_w
            y_val = y_min + frac * (y_max - y_min)
            y = top + plot_h - frac * plot_h
            x_val = x_min + frac * (x_max - x_min)
            parts.append(f'<line x1="{x:.2f}" y1="{top + plot_h}" x2="{x:.2f}" y2="{top + plot_h + 4}" stroke="black" stroke-width="1"/>')
            parts.append(_svg_text(x, top + plot_h + 18, f"{x_val:g}", size=9))
            parts.append(f'<line x1="{left - 4}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="black" stroke-width="1"/>')
            parts.append(_svg_text(left - 8, y + 3, f"{y_val:g}", size=9, anchor="end"))

        for index, (name, group_rows) in enumerate(groups.items()):
            points = []
            for row in group_rows:
                x = _scale(to_float(row[args.x], args.x), x_min, x_max, left, left + plot_w)
                y = _scale(to_float(row[args.y], args.y), y_min, y_max, top + plot_h, top)
                points.append((x, y))
            points.sort(key=lambda item: item[0])
            color = palette[index % len(palette)]
            if args.kind == "line" and len(points) > 1:
                d = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
                parts.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="1.8"/>')
            for x, y in points:
                parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{color}" stroke="white" stroke-width="0.6"/>')
            if args.group:
                lx = left + plot_w - 70
                ly = top + 12 + index * 16
                parts.append(f'<line x1="{lx}" y1="{ly - 4}" x2="{lx + 14}" y2="{ly - 4}" stroke="{color}" stroke-width="1.8"/>')
                parts.append(_svg_text(lx + 20, ly, name, size=9, anchor="start"))

    elif args.kind == "bar":
        categories = [row[args.x] for row in rows]
        values = [to_float(row[args.y], args.y) for row in rows]
        y_min, y_max = 0, max(values)
        y_pad = y_max * 0.08 or 1
        y_max += y_pad
        bar_w = plot_w / max(len(values), 1) * 0.62
        for idx, (category, value) in enumerate(zip(categories, values)):
            cx = left + (idx + 0.5) * plot_w / len(values)
            bar_h = _scale(value, y_min, y_max, 0, plot_h)
            x = cx - bar_w / 2
            y = top + plot_h - bar_h
            parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{bar_h:.2f}" fill="#4c78a8" stroke="black" stroke-width="0.6"/>')
            parts.append(_svg_text(cx, top + plot_h + 18, category, size=9))
        for tick in range(5):
            frac = tick / 4
            y_val = y_min + frac * (y_max - y_min)
            y = top + plot_h - frac * plot_h
            parts.append(f'<line x1="{left - 4}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="black" stroke-width="1"/>')
            parts.append(_svg_text(left - 8, y + 3, f"{y_val:g}", size=9, anchor="end"))

    parts.append(_svg_text(left + plot_w / 2, height - 12, args.xlabel or args.x, size=11))
    parts.append(_svg_text(14, top + plot_h / 2, args.ylabel or args.y, size=11, rotate=-90))
    parts.append("</svg>")
    args.output.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {args.output} (basic SVG fallback; install matplotlib for full nature-style rendering)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create editable SVG plots from CSV/TSV.")
    parser.add_argument("--input", required=True, type=Path, help="CSV/TSV input with header row")
    parser.add_argument("--output", required=True, type=Path, help="Output SVG path")
    parser.add_argument("--kind", choices=["line", "scatter", "bar", "box", "heatmap"], default="line")
    parser.add_argument("--x", required=True, help="X/category column")
    parser.add_argument("--y", required=True, help="Y/value column")
    parser.add_argument("--group", help="Optional grouping column")
    parser.add_argument("--title", help="Optional title")
    parser.add_argument("--xlabel", help="X-axis label")
    parser.add_argument("--ylabel", help="Y-axis label")
    parser.add_argument("--width", type=float, default=3.6, help="Figure width in inches")
    parser.add_argument("--height", type=float, default=2.7, help="Figure height in inches")
    parser.add_argument(
        "--palette",
        choices=sorted(PALETTES),
        default="nmi-pastel",
        help="Nature-style color family; default uses low-saturation NMI pastel colors",
    )
    parser.add_argument(
        "--no-install-deps",
        action="store_true",
        help="Do not auto-install matplotlib/numpy; use the basic SVG fallback when they are missing",
    )
    args = parser.parse_args()

    rows = read_rows(args.input)
    required = [args.x, args.y] + ([args.group] if args.group else [])
    missing = [key for key in required if key not in rows[0]]
    if missing:
        raise SystemExit(f"Missing column(s): {', '.join(missing)}")

    plt = import_matplotlib(auto_install=not args.no_install_deps)
    if plt is None:
        save_basic_svg(rows, args)
        return 0

    fig, ax = plt.subplots(figsize=(args.width, args.height), constrained_layout=True)
    n_colors = len(grouped(rows, args.group)) if args.group else max(len(rows), 1)
    colors = palette_colors(args.palette, n_colors)

    if args.kind in {"line", "scatter"}:
        plot_line_or_scatter(ax, rows, args.x, args.y, args.group, args.kind, colors)
    elif args.kind == "bar":
        plot_bar(ax, rows, args.x, args.y, args.group, colors)
    elif args.kind == "box":
        plot_box(ax, rows, args.x, args.y, args.group, colors)
    elif args.kind == "heatmap":
        image = plot_heatmap(ax, rows, args.x, args.y, args.group or args.y)
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    ax.set_xlabel(args.xlabel or args.x)
    ax.set_ylabel(args.ylabel or args.y)
    if args.title:
        ax.set_title(args.title, fontsize=10, pad=6)
    if args.group and args.kind != "heatmap":
        ax.legend(frameon=False, fontsize=8)
    fig.savefig(args.output, format="svg")
    plt.close(fig)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
