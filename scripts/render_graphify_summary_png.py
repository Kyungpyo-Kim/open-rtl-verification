#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render Graphify summary.json into a PNG report")
    p.add_argument("summary_json")
    p.add_argument("--output", required=True)
    p.add_argument("--title")
    return p.parse_args()


def load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def top_counts(items: list[dict], key: str, limit: int = 8) -> list[tuple[str, int]]:
    c = Counter()
    for item in items:
        value = item.get(key)
        if value:
            c[value] += 1
    return c.most_common(limit)


def top_files(files: list[dict], limit: int = 8) -> list[tuple[str, int]]:
    rows = sorted(files, key=lambda x: int(x.get("line_count", 0)), reverse=True)[:limit]
    return [(str(row.get("file", "")), int(row.get("line_count", 0))) for row in rows]


def render(summary: dict, output: Path, title: str) -> None:
    stats = summary.get("stats", {})
    entities = summary.get("entities", [])
    edges = summary.get("edges", [])
    files = summary.get("files", [])

    entity_counts = stats.get("entity_counts", {})
    edge_types = top_counts(edges, "type", limit=6)
    extend_targets = top_counts(entities, "extends", limit=8)
    biggest_files = top_files(files, limit=8)

    fig = plt.figure(figsize=(16, 10), dpi=150)
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], width_ratios=[1, 1])

    fig.suptitle(title, fontsize=20, fontweight="bold", y=0.98)

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.axis("off")
    summary_lines = [
        f"Files: {stats.get('file_count', 0)}",
        f"UVM files: {stats.get('uvm_file_count', 0)}",
        f"Entities: {sum(entity_counts.values())}",
        f"Edges: {stats.get('edge_count', 0)}",
    ]
    ax0.text(0.02, 0.92, "Snapshot", fontsize=16, fontweight="bold", va="top")
    ax0.text(0.02, 0.78, "\n".join(summary_lines), fontsize=14, va="top", family="monospace")

    ax1 = fig.add_subplot(gs[0, 1])
    kinds = list(entity_counts.keys())
    counts = [entity_counts[k] for k in kinds]
    colors = ["#2E86AB", "#A23B72", "#F18F01", "#4E937A", "#6C5CE7", "#E17055"][: len(kinds)]
    ax1.bar(kinds, counts, color=colors)
    ax1.set_title("Entity kinds")
    ax1.set_ylabel("count")
    for idx, value in enumerate(counts):
        ax1.text(idx, value, str(value), ha="center", va="bottom", fontsize=10)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.axis("off")
    ax2.text(0.02, 0.98, "Top inheritance / structure hints", fontsize=15, fontweight="bold", va="top")
    y = 0.88
    for name, count in extend_targets[:8]:
        ax2.text(0.03, y, f"- {name}: {count}", fontsize=12, va="top", family="monospace")
        y -= 0.09
    if not extend_targets:
        ax2.text(0.03, y, "- no inheritance edges detected", fontsize=12, va="top")
    y -= 0.05
    ax2.text(0.02, y, "Edge types", fontsize=15, fontweight="bold", va="top")
    y -= 0.1
    for name, count in edge_types:
        ax2.text(0.03, y, f"- {name}: {count}", fontsize=12, va="top", family="monospace")
        y -= 0.09

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_title("Largest files")
    file_names = [name[-42:] if len(name) > 42 else name for name, _ in biggest_files][::-1]
    file_counts = [count for _, count in biggest_files][::-1]
    ax3.barh(file_names, file_counts, color="#3D5A80")
    ax3.set_xlabel("lines")
    ax3.tick_params(axis="y", labelsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    args = parse_args()
    summary = load_summary(Path(args.summary_json))
    title = args.title or Path(args.summary_json).parent.name
    render(summary, Path(args.output), title)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
