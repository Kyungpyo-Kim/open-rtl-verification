#!/usr/bin/env python3
"""Minimal Graphify workflow runner for open-rtl-verification.

This script does three small but useful things:
1. Collects Verilog/SystemVerilog sources from a target directory.
2. Writes a stable manifest file for reproducible analysis inputs.
3. Optionally invokes an external Graphify CLI if available.

The command is intentionally lightweight so the repository can standardize
its analysis entrypoint before binding to one exact Graphify installation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_EXTENSIONS = (".v", ".vh", ".sv", ".svh")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect sources and optionally run Graphify on them."
    )
    parser.add_argument(
        "input",
        help="RTL/TB/UVM source directory to analyze",
    )
    parser.add_argument(
        "--output-dir",
        default="graph/graphify_outputs/latest",
        help="Directory for manifest and Graphify outputs",
    )
    parser.add_argument(
        "--graphify-bin",
        default="graphify",
        help="Graphify executable name or absolute path",
    )
    parser.add_argument(
        "--manifest-name",
        default="sources.json",
        help="Manifest filename written under output-dir",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=list(DEFAULT_EXTENSIONS),
        help="Source extensions to include",
    )
    parser.add_argument(
        "--graphify-args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Extra args passed through to Graphify after '--graphify-args'",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only write the manifest, do not invoke Graphify",
    )
    return parser.parse_args()


def collect_sources(root: Path, extensions: Iterable[str]) -> list[Path]:
    normalized = {ext if ext.startswith(".") else f".{ext}" for ext in extensions}
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in normalized
    )


def write_manifest(root: Path, output_dir: Path, manifest_name: str, sources: list[Path]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / manifest_name
    payload = {
        "input_root": str(root.resolve()),
        "source_count": len(sources),
        "sources": [str(path.resolve()) for path in sources],
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def run_graphify(graphify_bin: str, manifest_path: Path, output_dir: Path, passthrough: list[str]) -> int:
    resolved = shutil.which(graphify_bin) if not Path(graphify_bin).exists() else graphify_bin
    if not resolved:
        print(
            "GRAPHIFY_NOT_FOUND: manifest written, but Graphify CLI is unavailable.",
            file=sys.stderr,
        )
        return 2

    command = [resolved, "analyze", "--manifest", str(manifest_path), "--output-dir", str(output_dir)]
    command.extend(passthrough)
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    args = parse_args()
    input_root = Path(args.input).resolve()
    if not input_root.exists() or not input_root.is_dir():
        print(f"INPUT_DIR_NOT_FOUND: {input_root}", file=sys.stderr)
        return 1

    sources = collect_sources(input_root, args.extensions)
    if not sources:
        print(f"NO_SOURCES_FOUND: {input_root}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir).resolve()
    manifest_path = write_manifest(input_root, output_dir, args.manifest_name, sources)

    print(f"MANIFEST_WRITTEN: {manifest_path}")
    print(f"SOURCE_COUNT: {len(sources)}")

    if args.manifest_only:
        return 0

    return run_graphify(args.graphify_bin, manifest_path, output_dir, args.graphify_args)


if __name__ == "__main__":
    raise SystemExit(main())
