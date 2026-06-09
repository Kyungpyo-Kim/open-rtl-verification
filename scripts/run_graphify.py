#!/usr/bin/env python3
"""Graphify workflow runner for open-rtl-verification.

Features:
1. Collect Verilog/SystemVerilog sources from a local directory or a staged git repo.
2. Optionally honor simulator-style filelists.
3. Write a deterministic manifest for Graphify input.
4. Optionally invoke an external Graphify CLI if available.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urlparse

DEFAULT_EXTENSIONS = (".v", ".vh", ".sv", ".svh")
DEFAULT_EXCLUDES = (
    ".git",
    "build",
    "out",
    "dist",
    "docs",
    "doc",
    "generated",
    "gen",
    "vendor",
    ".venv",
    "venv",
    "__pycache__",
)
FILELIST_VAR_RE = re.compile(r"\$\(([^)]+)\)|\$([A-Za-z_][A-Za-z0-9_]*)")
REPO_ROOT = Path(__file__).resolve().parent.parent
VENDORED_GRAPHIFY_ROOT = REPO_ROOT / "vendor" / "graphify"
OPEN_TARGETS_CONFIG = REPO_ROOT / "configs" / "open_targets.json"
RENDER_HTML_TO_PNG = REPO_ROOT / "scripts" / "render_html_to_png.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect sources, write a Graphify manifest, and generate Graphify artifacts."
    )
    parser.add_argument("input", nargs="?", help="RTL/TB/UVM source directory or git URL to analyze")
    parser.add_argument(
        "--target",
        help="Named preset from configs/open_targets.json. Fills input/output/ref/sparse settings unless explicitly overridden.",
    )
    parser.add_argument(
        "--output-dir",
        default="graph/graphify_outputs/latest",
        help="Directory for the manifest and generated Graphify outputs",
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
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude during source collection. Can be repeated.",
    )
    parser.add_argument(
        "--filelist",
        help="Optional filelist (.f) to honor for ordering and exact source selection",
    )
    parser.add_argument(
        "--repo-ref",
        default="HEAD",
        help="Git ref to checkout when input is a git URL",
    )
    parser.add_argument(
        "--sparse-path",
        action="append",
        default=[],
        help="Sparse checkout path when input is a git URL. Can be repeated.",
    )
    parser.add_argument(
        "--staging-root",
        default=".cache/graphify_repos",
        help="Directory used to stage git repos for analysis",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Write manifest only, do not generate Graphify outputs",
    )
    parser.add_argument(
        "--graphify-source",
        choices=("auto", "vendor", "installed"),
        default="auto",
        help="Choose Graphify import source. 'auto' prefers the vendored fork when present.",
    )
    parser.add_argument(
        "--render-png",
        action="store_true",
        help="Also render graph.html to graph.png when Graphify output generation succeeds.",
    )
    return parser.parse_args()


def load_open_target(name: str, config_path: Path = OPEN_TARGETS_CONFIG) -> dict[str, Any]:
    if not config_path.is_file():
        raise RuntimeError(f"OPEN_TARGETS_CONFIG_NOT_FOUND: {config_path}")

    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"OPEN_TARGETS_CONFIG_INVALID: {config_path}: {exc}") from exc

    for target in payload.get("targets", []):
        if target.get("name") == name:
            return target

    available = ", ".join(sorted(target.get("name", "<unnamed>") for target in payload.get("targets", [])))
    raise RuntimeError(f"OPEN_TARGET_NOT_FOUND: {name}. Available: {available}")


def apply_open_target_defaults(args: argparse.Namespace) -> argparse.Namespace:
    if not args.target:
        return args

    target = load_open_target(args.target)
    if args.input is None:
        args.input = target.get("repo_url", args.input)
    if args.output_dir == "graph/graphify_outputs/latest":
        args.output_dir = target.get("output_dir", args.output_dir)
    if args.repo_ref == "HEAD":
        args.repo_ref = target.get("repo_ref", args.repo_ref)
    if not args.sparse_path:
        args.sparse_path = list(target.get("sparse_paths", []))
    return args


def configure_graphify_import(source: str) -> str:
    vendor_available = (VENDORED_GRAPHIFY_ROOT / "graphify").is_dir()
    if source == "installed":
        return "installed"
    if source == "vendor":
        if not vendor_available:
            raise RuntimeError(f"GRAPHIFY_VENDOR_NOT_FOUND: {VENDORED_GRAPHIFY_ROOT}")
        sys.path.insert(0, str(VENDORED_GRAPHIFY_ROOT))
        return "vendor"
    if vendor_available:
        sys.path.insert(0, str(VENDORED_GRAPHIFY_ROOT))
        return "vendor"
    return "installed"


def is_git_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "ssh"} or value.endswith(".git") or value.startswith("git@")


def run_command(command: Sequence[str], cwd: Path | None = None) -> None:
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"COMMAND_FAILED({completed.returncode}): {' '.join(command)}")


def stage_git_repo(repo_url: str, repo_ref: str, sparse_paths: Sequence[str], staging_root: Path) -> Path:
    repo_name = Path(urlparse(repo_url).path or repo_url.split(":")[-1]).name
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    safe_ref = re.sub(r"[^A-Za-z0-9_.-]+", "_", repo_ref)
    repo_dir = staging_root / f"{repo_name}-{safe_ref}"
    staging_root.mkdir(parents=True, exist_ok=True)

    if not repo_dir.exists():
        run_command(["git", "clone", "--depth", "1", "--no-checkout", repo_url, str(repo_dir)])
    else:
        run_command(["git", "fetch", "--depth", "1", "origin", repo_ref], cwd=repo_dir)

    run_command(["git", "checkout", "-f", repo_ref], cwd=repo_dir)

    if sparse_paths:
        run_command(["git", "sparse-checkout", "init", "--cone"], cwd=repo_dir)
        run_command(["git", "sparse-checkout", "set", *sparse_paths], cwd=repo_dir)
        run_command(["git", "checkout", "-f", repo_ref], cwd=repo_dir)

    return repo_dir.resolve()


def normalize_extensions(extensions: Iterable[str]) -> set[str]:
    return {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions}


def should_exclude(path: Path, root: Path, excluded_names: set[str]) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    return any(part in excluded_names for part in relative.parts[:-1])


def collect_sources(root: Path, extensions: Iterable[str], excluded_names: Iterable[str]) -> list[Path]:
    normalized_exts = normalize_extensions(extensions)
    excluded = set(excluded_names)
    sources: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in normalized_exts:
            continue
        if should_exclude(path, root, excluded):
            continue
        sources.append(path)
    return sorted(sources)


def substitute_vars(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1) or match.group(2)
        return str(Path.cwd()) if key == "PWD" else match.group(0)

    return FILELIST_VAR_RE.sub(repl, text)


def parse_filelist(filelist_path: Path, root: Path, extensions: Iterable[str]) -> list[Path]:
    normalized_exts = normalize_extensions(extensions)
    visited: set[Path] = set()
    resolved: list[Path] = []

    def walk(current: Path) -> None:
        current = current.resolve()
        if current in visited:
            return
        visited.add(current)
        for raw_line in current.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            line = substitute_vars(line)
            if line.startswith(("-f ", "-F ")):
                nested = line[2:].strip()
                nested_path = (current.parent / nested).resolve()
                walk(nested_path)
                continue
            if line.startswith("+incdir+"):
                continue
            token = line.split()[0]
            candidate = Path(token)
            if not candidate.is_absolute():
                candidate = (current.parent / candidate).resolve()
            if candidate.suffix.lower() in normalized_exts and candidate.exists():
                resolved.append(candidate)

    walk(filelist_path if filelist_path.is_absolute() else (root / filelist_path))
    deduped: list[Path] = []
    seen: set[Path] = set()
    for item in resolved:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def write_manifest(
    root: Path,
    output_dir: Path,
    manifest_name: str,
    sources: Sequence[Path],
    repo_url: str | None,
    repo_ref: str | None,
    filelist: str | None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / manifest_name
    payload = {
        "input_root": str(root.resolve()),
        "source_count": len(sources),
        "sources": [str(path.resolve()) for path in sources],
        "relative_sources": [relative_to_root(path, root) for path in sources],
        "repo_url": repo_url,
        "repo_ref": repo_ref,
        "filelist": filelist,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def run_graphify(manifest_path: Path, input_root: Path, output_dir: Path, sources: Sequence[Path]) -> int:
    try:
        from graphify.extract import extract
        from graphify.build import build_from_json
        from graphify.cluster import cluster, score_all
        from graphify.analyze import god_nodes, surprising_connections, suggest_questions
        from graphify.report import generate
        from graphify.export import to_html, to_json
    except ImportError:
        print(
            "GRAPHIFY_NOT_INSTALLED: install the official package with 'python3 -m pip install --user graphifyy' and rerun.",
            file=sys.stderr,
        )
        return 2

    code_sources = [path for path in sources if path.suffix.lower() in normalize_extensions(DEFAULT_EXTENSIONS)]
    if not code_sources:
        print("GRAPHIFY_NO_CODE_SOURCES: no supported Verilog/SystemVerilog files found in manifest.", file=sys.stderr)
        return 1

    extraction = extract(code_sources)
    graph = build_from_json(extraction)
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    labels = {cid: f"Community {cid}" for cid in communities}
    gods = god_nodes(graph)
    surprises = surprising_connections(graph, communities)
    questions = suggest_questions(graph, communities, labels)
    detection_result = {
        "total_files": len(sources),
        "total_words": 0,
        "files": {
            "code": [str(path) for path in code_sources],
        },
    }
    token_cost = {
        "input": extraction.get("input_tokens", 0),
        "output": extraction.get("output_tokens", 0),
    }
    report = generate(
        graph,
        communities,
        cohesion,
        labels,
        gods,
        surprises,
        detection_result,
        token_cost,
        str(input_root.resolve()),
        suggested_questions=questions,
    )
    (output_dir / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    to_json(graph, communities, str(output_dir / "graph.json"), force=True)
    to_html(graph, communities, str(output_dir / "graph.html"), community_labels=labels)
    return 0


def render_graph_png(output_dir: Path) -> int:
    html_path = output_dir / "graph.html"
    png_path = output_dir / "graph.png"
    if not html_path.is_file():
        print(f"GRAPH_HTML_NOT_FOUND: {html_path}", file=sys.stderr)
        return 1
    completed = subprocess.run(
        [sys.executable, str(RENDER_HTML_TO_PNG), str(html_path), "--output", str(png_path)],
        check=False,
    )
    return completed.returncode


def main() -> int:
    try:
        args = apply_open_target_defaults(parse_args())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not args.input:
        print("INPUT_REQUIRED: provide an input path/git URL or use --target with a preset repo_url", file=sys.stderr)
        return 2

    try:
        graphify_source = configure_graphify_import(args.graphify_source)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    output_dir = Path(args.output_dir).resolve()
    excluded_names = set(DEFAULT_EXCLUDES).union(args.exclude_dir)

    repo_url: str | None = None
    repo_ref: str | None = None
    if is_git_url(args.input):
        repo_url = args.input
        repo_ref = args.repo_ref
        input_root = stage_git_repo(args.input, args.repo_ref, args.sparse_path, Path(args.staging_root).resolve())
    else:
        input_root = Path(args.input).resolve()

    if not input_root.exists() or not input_root.is_dir():
        print(f"INPUT_DIR_NOT_FOUND: {input_root}", file=sys.stderr)
        return 1

    if args.filelist:
        filelist_path = Path(args.filelist)
        sources = parse_filelist(filelist_path, input_root, args.extensions)
    else:
        sources = collect_sources(input_root, args.extensions, excluded_names)

    if not sources:
        print(f"NO_SOURCES_FOUND: {input_root}", file=sys.stderr)
        return 1

    manifest_path = write_manifest(
        input_root,
        output_dir,
        args.manifest_name,
        sources,
        repo_url,
        repo_ref,
        args.filelist,
    )

    print(f"MANIFEST_WRITTEN: {manifest_path}")
    print(f"SOURCE_COUNT: {len(sources)}")
    print(f"GRAPHIFY_SOURCE: {graphify_source}")

    if args.manifest_only:
        return 0

    graphify_rc = run_graphify(manifest_path, input_root, output_dir, sources)
    if graphify_rc != 0:
        return graphify_rc

    if args.render_png:
        png_rc = render_graph_png(output_dir)
        if png_rc != 0:
            return png_rc
        print(f"PNG_WRITTEN: {output_dir / 'graph.png'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
