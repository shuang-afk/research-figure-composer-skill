# Nature-Skills Style Guide

Use this guide when the user asks for Nature-style figures, journal figures, SCI figures, mechanism figures, workflows, or polished research diagrams. It distills the installed `nature-figure` skill into the SVG-first workflow of `research-figure-composer`.

## Figure Contract

Before drawing, define:

- Core conclusion: one sentence with a verb.
- Archetype: `quantitative grid`, `schematic-led composite`, `image plate + quant`, or `asymmetric mixed-modality`.
- Panel map: every panel must answer a distinct scientific question.
- Evidence hierarchy: hero evidence first, validation second, controls/robustness quieter.
- Export target: primary SVG, editable text, source data/script retained.
- Reviewer risk: sample size, error-bar definition, statistics, traceability, image integrity.

Do not start from a favorite template. Start from the conclusion and evidence hierarchy, then choose the fewest panels that defend it.

## Mandatory SVG And Font Rules

For Python/Matplotlib outputs, set these before figure creation:

```python
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
```

Use final journal-density sizes by default:

- Base text: 7-9 pt for dense journal-width figures.
- Panel labels: small bold lowercase letters, about 8-9 pt.
- Axis line width: 0.8-1.2.
- No top/right spines.
- Frameless legends.
- No grid by default.

## Palettes

Use one neutral family, one signal family, and one accent family. Keep the same category color across all panels.

Semantic palette:

```python
PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral_light": "#CFCECE",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}
```

NMI pastel palette for dense multi-panel comparison pages:

```python
PALETTE_NMI_PASTEL = {
    "baseline_dark": "#484878",
    "baseline_mid": "#7884B4",
    "baseline_soft": "#B4C0E4",
    "ours_tiny": "#E4E4F0",
    "ours_base": "#E4CCD8",
    "ours_large": "#F0C0CC",
    "delta_up": "#2E9E44",
    "delta_down": "#E53935",
}
```

Modality rules:

- Mechanism/material: aqua, teal, lilac, soft violet; one red callout only.
- Imaging: black only inside image plates, gray context plus cyan/magenta channels.
- Clinical: black/dark baseline, restrained warm/cool follow-up colors, pale group bands.
- Genomics/systems: neutral greys plus one blue family and one red family.
- Reserve red/green for direction, gain/loss, thresholds, and biological signs; do not use red/green as the only category encoding.

## Layout Rules

- White background for charts and diagrams; black only for microscopy/image plates.
- Prefer one dominant hero panel over equal-sized dashboards when the science is asymmetric.
- For schematic-led figures, allocate 45-60% of figure height to the schematic and make supporting plots quieter.
- Use direct labels or one shared legend strip when repeated legends would waste space.
- Hide x-tick labels when methods are already named by a legend or direct labels.
- Tighten y-limits to the data range when fixed 0-100 scales obscure differences.
- Use hatching or line style in addition to color when grayscale printing matters.

## Diagram And Workflow SVG Rules

For editable hand-authored SVG diagrams:

- Use thin black/neutral strokes, white or very pale fills, and a single accent family.
- Use small lowercase panel letters, not large badges.
- Avoid decorative cards, heavy colored blocks, shadows, gradients, and busy borders.
- Use alignment, whitespace, and arrow direction to express structure.
- Keep node labels short; move explanatory text to captions or notes.
- Reuse the same color mapping between schematic nodes and any quantitative panels.

## QA Before Delivery

Run `scripts/validate_svg.py <figure.svg>` and check:

- Text remains as `<text>` elements.
- `image=0` for vector-only diagrams and data plots unless a real image panel is intentional.
- No label overlaps at final size.
- Figure has a `viewBox`.
- Source `.py`, `.drawio`, spec, or data file is retained beside the SVG.

When final submission is the target, also export PDF/TIFF if requested, but keep SVG primary.
