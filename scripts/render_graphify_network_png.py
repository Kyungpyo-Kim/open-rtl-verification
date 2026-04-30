#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render Graphify summary.json as a node-edge PNG")
    p.add_argument("summary_json")
    p.add_argument("--output", required=True)
    p.add_argument("--title")
    p.add_argument("--max-nodes", type=int, default=28)
    return p.parse_args()


def shorten(label: str, max_len: int = 26) -> str:
    if len(label) <= max_len:
        return label
    return label[: max_len - 3] + "..."


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def choose_nodes(data: dict, max_nodes: int) -> list[str]:
    score = Counter()
    for entity in data.get("entities", []):
        score[entity.get("name", "")] += 4
        ext = entity.get("extends")
        if ext:
            score[ext] += 2
    for edge in data.get("edges", []):
        score[edge.get("from", "")] += 2
        score[edge.get("to", "")] += 2
        if edge.get("type") == "extends":
            score[edge.get("from", "")] += 2
            score[edge.get("to", "")] += 2
    score.pop("", None)
    return [name for name, _ in score.most_common(max_nodes)]


def node_kinds(data: dict) -> dict[str, str]:
    kinds = {}
    for entity in data.get("entities", []):
        name = entity.get("name")
        kind = entity.get("kind")
        if name and kind and name not in kinds:
            kinds[name] = kind
    return kinds


def pick_edges(data: dict, chosen: set[str], limit: int = 60) -> list[dict]:
    picked = []
    seen = set()
    for edge in data.get("edges", []):
        a = edge.get("from", "")
        b = edge.get("to", "")
        if a in chosen and b in chosen:
            key = (a, b, edge.get("type", ""))
            if key not in seen:
                seen.add(key)
                picked.append(edge)
    picked.sort(key=lambda e: {"extends": 0, "instantiates": 1, "imports": 2}.get(e.get("type", ""), 9))
    return picked[:limit]


def layout(nodes: list[str]) -> dict[str, tuple[float, float]]:
    n = len(nodes)
    pos = {}
    if n == 0:
        return pos
    rings = []
    if n <= 10:
        rings = [nodes]
    elif n <= 24:
        rings = [nodes[:8], nodes[8:]]
    else:
        rings = [nodes[:8], nodes[8:20], nodes[20:]]
    radii = [0.9, 1.7, 2.45]
    for ring_idx, ring_nodes in enumerate(rings):
        radius = radii[ring_idx]
        for i, node in enumerate(ring_nodes):
            ang = (2 * math.pi * i / len(ring_nodes)) + ring_idx * 0.25
            pos[node] = (radius * math.cos(ang), radius * math.sin(ang))
    return pos


def render(data: dict, output: Path, title: str, max_nodes: int) -> None:
    nodes = choose_nodes(data, max_nodes)
    chosen = set(nodes)
    edges = pick_edges(data, chosen)
    kinds = node_kinds(data)
    pos = layout(nodes)

    fig, ax = plt.subplots(figsize=(16, 16), dpi=160)
    ax.set_title(title, fontsize=20, fontweight="bold", pad=20)
    ax.axis("off")

    edge_colors = {"extends": "#6C5CE7", "instantiates": "#0984E3", "imports": "#00B894"}
    node_colors = {"class": "#FDCB6E", "module": "#74B9FF", "package": "#A29BFE", "interface": "#55EFC4"}

    for edge in edges:
        a = edge.get("from")
        b = edge.get("to")
        if a not in pos or b not in pos:
            continue
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        color = edge_colors.get(edge.get("type", ""), "#636E72")
        patch = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=12,
                                linewidth=1.6, color=color, alpha=0.65,
                                connectionstyle="arc3,rad=0.08")
        ax.add_patch(patch)

    for node in nodes:
        x, y = pos[node]
        kind = kinds.get(node, "other")
        color = node_colors.get(kind, "#DFE6E9")
        ax.scatter([x], [y], s=2200, c=color, edgecolors="#2D3436", linewidths=1.5, zorder=3)
        ax.text(x, y, shorten(node), ha="center", va="center", fontsize=9, zorder=4)

    legend_lines = [
        f"nodes shown: {len(nodes)}",
        f"edges shown: {len(edges)}",
        "edge colors: extends / instantiates / imports",
    ]
    ax.text(-3.1, 3.0, "\n".join(legend_lines), fontsize=11, va="top", family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#F8F9FA", edgecolor="#B2BEC3"))

    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.3, 3.3)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    args = parse_args()
    data = load(Path(args.summary_json))
    title = args.title or Path(args.summary_json).parent.name
    render(data, Path(args.output), title, args.max_nodes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
