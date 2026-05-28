# AutoFigure-Edit Workflow

Use AutoFigure-Edit for advanced prose-to-figure drafting when the user provides method text, a paper abstract, a model description, or a visual concept that would take too long to build manually from scratch.

## When To Use

- Fast first draft of a scientific schematic from natural language.
- Method or pipeline figure from a paragraph.
- Editable SVG draft that will be cleaned by Codex afterward.

Do not use it for ordinary CSV plots; use the Nature/Matplotlib route instead.

## Procedure

1. Convert the request into a structured visual prompt:
   - field/domain
   - intended audience
   - panels
   - entities and relationships
   - exact labels to include
   - forbidden labels or visual claims
2. Generate an editable SVG using AutoFigure-Edit if the local service or repo is available.
3. Inspect the SVG structure:
   - text remains text
   - labels are accurate
   - no invented biological/technical claims
   - no raster-only full-figure image
4. Edit or rebuild wrong parts in SVG/Draw.io/Python as needed.
5. Run `scripts/validate_svg.py` before delivery.

## Local Availability Check

Search likely locations before assuming installation:

```powershell
Get-ChildItem -Path $HOME, "$HOME\Documents", "$HOME\Desktop" -Recurse -Directory -Filter "*AutoFigure*" -ErrorAction SilentlyContinue
```

If AutoFigure-Edit is not installed, create a clean SVG or Draw.io figure directly and note that AutoFigure was unavailable. Do not block the task.

## Prompt Template

```text
Create an editable SVG scientific figure.
Domain:
Purpose:
Audience:
Panels:
Entities:
Relationships/arrows:
Required labels:
Style: clean journal figure, white background, editable text, restrained color palette.
Avoid: raster-only figure, decorative stock-art look, unsupported claims.
```
