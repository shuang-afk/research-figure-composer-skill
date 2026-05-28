#!/usr/bin/env python3
"""Validate and lightly normalize editable SVG research figures."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def _tag_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _iter(root: ET.Element, name: str):
    for element in root.iter():
        if _tag_name(element.tag) == name:
            yield element


def _parse_svg(path: Path) -> ET.ElementTree:
    try:
        return ET.parse(path)
    except ET.ParseError as exc:
        raise SystemExit(f"Invalid SVG XML: {exc}") from exc


def add_background(root: ET.Element, color: str) -> None:
    width = root.get("width", "100%")
    height = root.get("height", "100%")
    rect = ET.Element(
        f"{{{SVG_NS}}}rect",
        {
            "x": "0",
            "y": "0",
            "width": width,
            "height": height,
            "fill": color,
        },
    )
    root.insert(0, rect)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SVG and report editability signals.")
    parser.add_argument("svg", type=Path, help="SVG file to validate")
    parser.add_argument("--output", type=Path, help="Optional path for normalized SVG")
    parser.add_argument("--strip-size", action="store_true", help="Remove width/height and keep viewBox for responsive SVG")
    parser.add_argument("--background", help="Add a full-canvas background fill color, e.g. white or #ffffff")
    args = parser.parse_args()

    if not args.svg.exists():
        raise SystemExit(f"SVG not found: {args.svg}")

    tree = _parse_svg(args.svg)
    root = tree.getroot()
    if _tag_name(root.tag) != "svg":
        raise SystemExit("Root element is not <svg>.")

    text_count = sum(1 for _ in _iter(root, "text"))
    image_count = sum(1 for _ in _iter(root, "image"))
    path_count = sum(1 for _ in _iter(root, "path"))
    group_count = sum(1 for _ in _iter(root, "g"))
    has_viewbox = root.get("viewBox") is not None

    warnings: list[str] = []
    if text_count == 0:
        warnings.append("No <text> elements found; labels may have been converted to paths.")
    if image_count > 0:
        warnings.append(f"{image_count} raster/embedded image element(s) found; verify the figure is not raster-only.")
    if not has_viewbox:
        warnings.append("No viewBox found; scaling may be less portable.")

    if args.strip_size:
        root.attrib.pop("width", None)
        root.attrib.pop("height", None)
    if args.background:
        add_background(root, args.background)

    output = args.output or (args.svg if (args.strip_size or args.background) else None)
    if output:
        tree.write(output, encoding="utf-8", xml_declaration=True)

    print(f"SVG: {args.svg}")
    print(f"text={text_count} image={image_count} path={path_count} group={group_count} viewBox={has_viewbox}")
    if output:
        print(f"wrote={output}")
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
