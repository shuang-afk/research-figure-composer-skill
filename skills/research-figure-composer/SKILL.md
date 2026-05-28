---
name: research-figure-composer
description: Create editable SVG research figures for papers, reports, presentations, and grant materials. Use when Codex needs to make or revise scientific schematics, mechanism diagrams, method diagrams, workflow figures, architecture diagrams, multi-panel data figures, Nature-style plots, journal-style scientific figures, or text-to-figure drafts. Routes schematic work through Draw.io-compatible SVG/.drawio, data figures through installed nature-figure-informed Matplotlib SVG, and advanced natural-language figure drafting through AutoFigure-Edit-style editable SVG.
---

# Research Figure Composer

Use this skill to produce research figures whose final deliverable is editable SVG. Prefer source-preserving outputs in this order: `.drawio` + `.svg` for diagrams, `.py` + `.svg` for data plots, and AutoFigure-Edit generated `.svg` plus prompt/spec notes for advanced text-to-figure work.

For any request that says "Nature style", "论文风格", "高水平期刊", "SCI figure", "机制图", or "流程图要像 Nature", read `references/nature-skills-style-guide.md` before drawing. The local `nature-figure` skill is installed as a deeper source for Matplotlib/R publication-figure conventions; use it when a task is primarily a journal-ready data figure.

## Mandatory Intake Round

Before generating a final figure from a new user request, do one short intake round:

1. Ask what figure type they want.
2. Show relevant saved figure-type examples from `references/example-gallery.md`.
3. Show concrete palette comparison images from `assets/examples/palette-data.svg` or `assets/examples/palette-diagram.svg`; do not ask the user to choose a palette from names alone.
4. Ask for the minimum details needed to generate: figure type, language, chosen palette preview/cell, core conclusion, and data/nodes/content.
5. Wait for the user's answer, then generate the figure.

Only skip this intake when the user explicitly says "直接生成", "跳过确认", "不用问", or equivalent. If the request already names a type, still show 2-3 closest examples and ask the user to confirm style/content before drawing.

## Route

1. **Schematic / method / mechanism / architecture figure**
   - Use Draw.io-compatible XML as the editable source.
   - Deliver both `<name>.drawio` and `<name>.svg` when possible.
   - Read `references/drawio-svg-workflow.md` if building a diagram from text.
   - Apply the diagram rules in `references/nature-skills-style-guide.md`: white background, thin neutral strokes, pale fills, short labels, one semantic accent family, no decorative cards.

2. **Data figure / statistical plot / multi-panel result figure**
   - Use Python Matplotlib with Nature-style rcParams and SVG text kept editable.
   - Let `scripts/nature_svg_plot.py` auto-install `matplotlib` and `numpy` when they are missing; only use `--no-install-deps` when package installation is explicitly unwanted.
   - Use the default `nmi-pastel` palette for related method families and `semantic` for clearly distinct biological/experimental roles.
   - Start from `scripts/nature_svg_plot.py` when the input is CSV/TSV or a simple table.
   - Deliver `<name>.py`, `<name>.svg`, and any cleaned input table.
   - Read `references/nature-figure-style.md` before styling multi-panel figures.

3. **Advanced text-to-SVG figure draft**
   - Use AutoFigure-Edit when the user wants a paper-method figure from prose, a visually composed scientific schematic, or a fast editable SVG first draft.
   - Treat AutoFigure output as a draft: inspect the SVG, fix labels/layout, then run `scripts/validate_svg.py`.
   - Read `references/autofigure-edit-workflow.md` for setup and handoff rules.

4. **Unclear or mixed request**
   - Use the mandatory intake round first.
   - Produce a small figure plan after the user answers: panels, source route for each panel, expected files.
   - Then implement each panel with the route above and combine into one final SVG when practical.

## Output Rules

- Always make the final visible deliverable an `.svg`.
- Keep text editable. For Matplotlib set `svg.fonttype = none`; for exported SVGs prefer embedded metadata/source XML when supported.
- Avoid raster-only output unless the user explicitly asks. If a raster input is unavoidable, place it as a trace/reference and rebuild editable shapes/text around it.
- Use short, publication-safe labels. Do not fill figures with explanatory prose.
- Prefer black/gray plus a restrained accent palette. Use color only to encode group, condition, stage, or emphasis.
- Keep every figure reproducible: save the source spec, `.drawio`, or `.py` beside the SVG.

## Implementation Checklist

1. Identify the figure type and choose the route.
2. Create a working folder named after the task if no folder exists.
3. Generate or edit the source artifact (`.drawio`, `.py`, or AutoFigure SVG/spec).
4. Export or save the final SVG.
5. Run `scripts/validate_svg.py <svg-path>` before delivery.
6. Open or inspect the SVG if layout risk is high: long labels, dense panels, custom fonts, or mixed vector/raster assets.

## Bundled Scripts

- `scripts/nature_svg_plot.py`: create editable SVG line, scatter, bar, box, or heatmap figures from CSV/TSV data using Matplotlib, auto-installing `matplotlib` and `numpy` by default.
- `scripts/validate_svg.py`: validate an SVG, report text/raster/path counts, optionally strip dimensions or add a white background.

## References

- `references/example-gallery.md`: saved example SVGs and the mandatory intake prompt template.
- `references/drawio-svg-workflow.md`: Draw.io route for editable schematic and workflow figures.
- `references/nature-figure-style.md`: data-figure conventions and Matplotlib settings.
- `references/nature-skills-style-guide.md`: distilled `nature-figure` style rules, palettes, layout patterns, and QA checks.
- `references/autofigure-edit-workflow.md`: AutoFigure-Edit route for text-to-editable-SVG drafts.
