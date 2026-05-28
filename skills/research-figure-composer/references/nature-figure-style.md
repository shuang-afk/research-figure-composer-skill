# Nature-Style Data Figure Workflow

Use this route for quantitative research figures: line plots, scatter plots, bar charts, box plots, heatmaps, multi-panel comparisons, ablation studies, and statistical summaries. For Nature-style figures, read `nature-skills-style-guide.md` first and treat the figure as a claim-driven visual argument.

## Required Matplotlib Settings

Use SVG with editable text:

```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 7,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
})
```

If Arial is unavailable, fall back to DejaVu Sans or Liberation Sans.

## Style Rules

- Prefer compact, print-readable panels.
- Label axes with units when known.
- Remove chartjunk: heavy grids, decorative shadows, 3D effects, and redundant legends.
- Use direct labels when that is clearer than a legend.
- For multi-panel figures, use panel letters `A`, `B`, `C` in bold near the upper-left of each panel.
- Use the installed `nature-figure` palette logic: neutral + signal + accent; default to low-saturation NMI pastel for related method families.
- Reserve green/red for direction, gain/loss, thresholds, or biological signs; do not rely on red/green alone for category identity.

## Script

Use `scripts/nature_svg_plot.py` for common CSV/TSV plots:

```powershell
python scripts/nature_svg_plot.py --input data.csv --output figure.svg --kind line --x time --y value --group condition --palette nmi-pastel
```

The script auto-installs `matplotlib` and `numpy` with the active Python when either package is missing. Use `--no-install-deps` only when package installation is not allowed; that mode can fall back to a simpler pure-SVG renderer for line, scatter, and bar figures.

For complex figures, copy the generated script pattern into a task-specific `.py` file and edit there. Deliver both the Python source and SVG.

## Verification

Run:

```powershell
python scripts/validate_svg.py figure.svg
```

Check that text elements exist. If every label is converted to paths, regenerate with `svg.fonttype = none`.
