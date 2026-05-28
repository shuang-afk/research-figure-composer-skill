# Draw.io SVG Workflow

Use this route for diagrams that need precise manual editing later: workflows, method pipelines, system architecture, model diagrams, mechanism maps, and figure panels with boxes/arrows/icons.

## Preferred Outputs

- Source: `<figure-name>.drawio`
- Final: `<figure-name>.svg`
- Optional preview: `<figure-name>.png`

If the installed Draw.io CLI supports it, export SVG with embedded diagram data so the SVG can be reopened in Draw.io and edited.

## Build Procedure

1. Convert the user's request into a concise figure spec:
   - title or panel label
   - nodes and groups
   - directed edges
   - labels
   - legend or color encoding
2. Create a `.drawio` source file using mxGraph XML or use the Draw.io MCP/CLI if available.
3. Use consistent geometry:
   - left-to-right for workflows
   - top-to-bottom for hierarchy
   - grouped lanes for phases, modules, datasets, or cohorts
4. Keep labels short enough to edit and read in print.
5. Export to SVG.
6. Run `scripts/validate_svg.py` on the SVG.

## Visual Defaults

- Canvas: white or transparent, sized to the target use.
- Shapes: rectangular or subtly rounded only when they represent process nodes; keep radius small.
- Arrows: direct orthogonal connectors for workflows, curved connectors only for feedback loops.
- Colors: neutral outlines plus one restrained semantic accent family; use red/green only for direction or risk signals.
- Text: use common fonts such as Arial, Helvetica, or DejaVu Sans.
- Nature-style diagrams: thin strokes, pale fills, no shadows, no gradients, no decorative cards, short labels, and small lowercase panel letters.

## Fallback Without Draw.io CLI

If Draw.io is not installed or export is unavailable, create the final SVG directly with structured XML, then preserve a Markdown or JSON figure spec beside it. Do not fake a `.drawio` file unless it can be opened by Draw.io.
