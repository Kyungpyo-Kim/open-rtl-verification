#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from html import escape
from pathlib import Path

EDGE_COLORS = {
    "extends": "#6c5ce7",
    "instantiates": "#0984e3",
    "imports": "#00b894",
}
NODE_COLORS = {
    "class": "#fdcb6e",
    "module": "#74b9ff",
    "package": "#a29bfe",
    "interface": "#55efc4",
    "other": "#dfe6e9",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render Graphify summary.json as standalone HTML")
    p.add_argument("summary_json")
    p.add_argument("--output", required=True)
    p.add_argument("--title")
    p.add_argument("--max-nodes", type=int, default=28)
    return p.parse_args()


def choose_nodes(data: dict, max_nodes: int) -> list[str]:
    score = Counter()
    for entity in data.get("entities", []):
        name = entity.get("name", "")
        if name:
            score[name] += 4
        ext = entity.get("extends")
        if ext:
            score[ext] += 2
    for edge in data.get("edges", []):
        a = edge.get("from", "")
        b = edge.get("to", "")
        if a:
            score[a] += 2
        if b:
            score[b] += 2
        if edge.get("type") == "extends":
            if a:
                score[a] += 2
            if b:
                score[b] += 2
    score.pop("", None)
    return [name for name, _ in score.most_common(max_nodes)]


def node_kinds(data: dict) -> dict[str, str]:
    out = {}
    for entity in data.get("entities", []):
        name = entity.get("name")
        kind = entity.get("kind")
        if name and kind and name not in out:
            out[name] = kind
    return out


def pick_edges(data: dict, chosen: set[str], limit: int = 80) -> list[dict]:
    picked = []
    seen = set()
    for edge in data.get("edges", []):
        a = edge.get("from", "")
        b = edge.get("to", "")
        t = edge.get("type", "")
        if a in chosen and b in chosen:
            key = (a, b, t)
            if key not in seen:
                seen.add(key)
                picked.append(edge)
    picked.sort(key=lambda e: {"extends": 0, "instantiates": 1, "imports": 2}.get(e.get("type", ""), 9))
    return picked[:limit]


def layout(nodes: list[str]) -> dict[str, tuple[float, float]]:
    n = len(nodes)
    if n == 0:
        return {}
    if n <= 10:
        rings = [nodes]
    elif n <= 24:
        rings = [nodes[:8], nodes[8:]]
    else:
        rings = [nodes[:8], nodes[8:20], nodes[20:]]
    radii = [150, 280, 400]
    pos = {}
    for ring_idx, ring_nodes in enumerate(rings):
        radius = radii[ring_idx]
        for i, node in enumerate(ring_nodes):
            ang = (2 * math.pi * i / len(ring_nodes)) + ring_idx * 0.23
            pos[node] = (radius * math.cos(ang), radius * math.sin(ang))
    return pos


def html(data: dict, title: str, max_nodes: int) -> str:
    stats = data.get("stats", {})
    kinds = node_kinds(data)
    nodes = choose_nodes(data, max_nodes)
    chosen = set(nodes)
    edges = pick_edges(data, chosen)
    pos = layout(nodes)

    width = 1200
    height = 1000
    cx = width / 2
    cy = height / 2

    svg_parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">']
    svg_parts.append('<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#636e72"/></marker></defs>')

    for edge in edges:
        a = edge["from"]
        b = edge["to"]
        if a not in pos or b not in pos:
            continue
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        color = EDGE_COLORS.get(edge.get("type", ""), "#636e72")
        svg_parts.append(
            f'<line x1="{cx + x1:.1f}" y1="{cy + y1:.1f}" x2="{cx + x2:.1f}" y2="{cy + y2:.1f}" stroke="{color}" stroke-width="2" stroke-opacity="0.7" marker-end="url(#arrow)" />'
        )

    for node in nodes:
        x, y = pos[node]
        kind = kinds.get(node, "other")
        color = NODE_COLORS.get(kind, NODE_COLORS["other"])
        sx = cx + x
        sy = cy + y
        label = escape(node)
        svg_parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="34" fill="{color}" stroke="#2d3436" stroke-width="2" />')
        svg_parts.append(f'<text x="{sx:.1f}" y="{sy:.1f}" text-anchor="middle" dominant-baseline="middle" font-size="11" font-family="Arial, sans-serif">{label[:24]}</text>')

    svg_parts.append("</svg>")
    svg = "\n".join(svg_parts)

    legend = "".join(
        f'<li><span class="swatch" style="background:{c}"></span>{escape(k)}</li>' for k, c in EDGE_COLORS.items()
    )

    kind_rows = "".join(
        f"<li>{escape(k)}: {v}</li>" for k, v in stats.get("entity_counts", {}).items()
    )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>{escape(title)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }}
header {{ padding: 24px 28px 8px; }}
main {{ display: grid; grid-template-columns: 320px 1fr; gap: 20px; padding: 0 28px 28px; }}
.card {{ background: white; border: 1px solid #dfe6e9; border-radius: 14px; padding: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.06); }}
.stats li, .kinds li, .legend li {{ margin: 8px 0; }}
.legend {{ list-style: none; padding: 0; }}
.swatch {{ display: inline-block; width: 14px; height: 14px; border-radius: 3px; margin-right: 8px; vertical-align: middle; }}
svg {{ background: white; border-radius: 14px; border: 1px solid #dfe6e9; box-shadow: 0 8px 24px rgba(0,0,0,0.06); }}
.small {{ color: #636e72; font-size: 13px; }}
</style>
</head>
<body>
<header>
  <h1>{escape(title)}</h1>
  <div class=\"small\">Standalone HTML network view generated from Graphify summary output.</div>
</header>
<main>
  <section class=\"card\">
    <h2>Snapshot</h2>
    <ul class=\"stats\">
      <li>Files: {stats.get('file_count', 0)}</li>
      <li>UVM files: {stats.get('uvm_file_count', 0)}</li>
      <li>Edges: {stats.get('edge_count', 0)}</li>
      <li>Nodes shown: {len(nodes)}</li>
      <li>Edges shown: {len(edges)}</li>
    </ul>
    <h3>Entity kinds</h3>
    <ul class=\"kinds\">{kind_rows}</ul>
    <h3>Edge colors</h3>
    <ul class=\"legend\">{legend}</ul>
  </section>
  <section>
    {svg}
  </section>
</main>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    data = json.loads(Path(args.summary_json).read_text(encoding="utf-8"))
    title = args.title or Path(args.summary_json).parent.name
    Path(args.output).write_text(html(data, title, args.max_nodes), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
