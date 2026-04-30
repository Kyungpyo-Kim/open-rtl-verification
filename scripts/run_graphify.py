#!/usr/bin/env python3
"""Enhanced Graphify workflow runner for open-rtl-verification.

Features:
1. Collect Verilog/SystemVerilog sources from a local directory or a staged git repo.
2. Optionally honor simulator-style filelists.
3. Write a deterministic manifest for Graphify input.
4. Generate a lightweight structural summary plus Markdown, HTML, and PNG visualizations.
5. Optionally invoke an external Graphify CLI if available.

The summary/visualization layer is intentionally heuristic. It gives the project a
reviewable, reproducible artifact even when Graphify output format differs between
machines or Graphify itself is not installed yet.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence
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
ENTITY_PATTERNS = {
    "module": re.compile(r"\bmodule\s+(\w+)"),
    "interface": re.compile(r"\binterface\s+(\w+)"),
    "package": re.compile(r"\bpackage\s+(\w+)"),
    "class": re.compile(r"\bclass\s+(\w+)(?:\s+extends\s+(\w+(?:::\w+)?))?"),
}
IMPORT_RE = re.compile(r"\bimport\s+(\w+(?:::\*)?)\s*;")
INSTANTIATION_RE = re.compile(
    r"(?m)^\s*(?!if\b|for\b|while\b|case\b|return\b|assign\b)(\w+)\s*(?:#\s*\([^;]*?\))?\s+(\w+)\s*\(",
    re.DOTALL,
)
UVM_MACRO_RE = re.compile(r"`uvm_[a-zA-Z0-9_]+")
RUN_TEST_RE = re.compile(r"\brun_test\s*\(")
CONFIG_DB_RE = re.compile(r"\buvm_config_db\s*#")
ANALYSIS_PORT_RE = re.compile(r"\buvm_analysis_(?:port|imp|export)\b")
VIF_RE = re.compile(r"\bvirtual\s+\w+\b")
COMMENT_LINE_RE = re.compile(r"//.*?$", re.MULTILINE)
COMMENT_BLOCK_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
DEFINE_RE = re.compile(r"^\s*`define\s+(\w+)\b", re.MULTILINE)
FILELIST_VAR_RE = re.compile(r"\$\(([^)]+)\)|\$([A-Za-z_][A-Za-z0-9_]*)")
RESERVED_TOKENS = {
    "always",
    "always_comb",
    "always_ff",
    "always_latch",
    "assign",
    "automatic",
    "begin",
    "case",
    "casex",
    "casez",
    "class",
    "else",
    "end",
    "endcase",
    "endclass",
    "endfunction",
    "endgenerate",
    "endmodule",
    "endinterface",
    "endpackage",
    "endtask",
    "for",
    "foreach",
    "forever",
    "fork",
    "function",
    "generate",
    "if",
    "initial",
    "interface",
    "join",
    "join_any",
    "join_none",
    "module",
    "package",
    "program",
    "repeat",
    "return",
    "task",
    "typedef",
    "while",
}


@dataclass(slots=True)
class Entity:
    kind: str
    name: str
    file: str
    extends: str | None = None


@dataclass(slots=True)
class AnalysisSummary:
    entities: list[Entity] = field(default_factory=list)
    edges: list[dict[str, str]] = field(default_factory=list)
    file_summaries: list[dict[str, object]] = field(default_factory=list)
    stats: dict[str, object] = field(default_factory=dict)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect sources, generate structural summaries, and optionally run Graphify."
    )
    parser.add_argument("input", help="RTL/TB/UVM source directory or git URL to analyze")
    parser.add_argument(
        "--output-dir",
        default="graph/graphify_outputs/latest",
        help="Directory for manifest, summaries, visualizations, and Graphify outputs",
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
        "--summary-name",
        default="summary.json",
        help="Heuristic analysis summary filename written under output-dir",
    )
    parser.add_argument(
        "--visualization-name",
        default="graph.md",
        help="Markdown visualization filename written under output-dir",
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
        "--graphify-args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Extra args passed through to Graphify after '--graphify-args'",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Write manifest/summary/visualization only, do not invoke Graphify",
    )
    return parser.parse_args()


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
            if line.startswith("-f "):
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


def strip_comments(text: str) -> str:
    return COMMENT_BLOCK_RE.sub("", COMMENT_LINE_RE.sub("", text))


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def analyze_sources(root: Path, sources: Sequence[Path]) -> AnalysisSummary:
    summary = AnalysisSummary()
    entity_index: dict[str, Entity] = {}
    edge_seen: set[tuple[str, str, str]] = set()
    file_summaries: list[dict[str, object]] = []
    entity_counter: Counter[str] = Counter()
    uvm_file_count = 0

    for source in sources:
        text = source.read_text(encoding="utf-8", errors="ignore")
        stripped = strip_comments(text)
        rel = relative_to_root(source, root)
        file_entities: list[dict[str, str]] = []
        local_names: set[str] = set()
        has_uvm = bool(UVM_MACRO_RE.search(stripped) or "uvm_" in stripped)
        if has_uvm:
            uvm_file_count += 1

        for kind, pattern in ENTITY_PATTERNS.items():
            for match in pattern.finditer(stripped):
                name = match.group(1)
                extends = match.group(2) if kind == "class" and match.lastindex and match.lastindex >= 2 else None
                entity = Entity(kind=kind, name=name, file=rel, extends=extends)
                summary.entities.append(entity)
                entity_index[name] = entity
                entity_counter[kind] += 1
                local_names.add(name)
                file_entities.append({"kind": kind, "name": name, **({"extends": extends} if extends else {})})
                if extends:
                    key = (name, extends, "extends")
                    if key not in edge_seen:
                        edge_seen.add(key)
                        summary.edges.append({"from": name, "to": extends, "type": "extends"})

        imports = [match.group(1) for match in IMPORT_RE.finditer(stripped)]
        instantiations = []
        for match in INSTANTIATION_RE.finditer(stripped):
            instantiated_type, instance_name = match.groups()
            if instantiated_type in local_names:
                continue
            if instantiated_type.lower() in RESERVED_TOKENS or instance_name.lower() in RESERVED_TOKENS:
                continue
            instantiations.append({"type": instantiated_type, "instance": instance_name})
            key = (rel, instantiated_type, "instantiates")
            if key not in edge_seen:
                edge_seen.add(key)
                summary.edges.append({"from": rel, "to": instantiated_type, "type": "instantiates"})

        file_summary = {
            "file": rel,
            "line_count": len(text.splitlines()),
            "entities": file_entities,
            "imports": imports,
            "instantiations": instantiations,
            "has_uvm": has_uvm,
            "has_run_test": bool(RUN_TEST_RE.search(stripped)),
            "has_config_db": bool(CONFIG_DB_RE.search(stripped)),
            "has_virtual_interface": bool(VIF_RE.search(stripped)),
            "has_analysis_port": bool(ANALYSIS_PORT_RE.search(stripped)),
            "defines": sorted(set(DEFINE_RE.findall(text))),
        }
        file_summaries.append(file_summary)

        for imported in imports:
            key = (rel, imported, "imports")
            if key not in edge_seen:
                edge_seen.add(key)
                summary.edges.append({"from": rel, "to": imported, "type": "imports"})

    summary.file_summaries = sorted(file_summaries, key=lambda item: str(item["file"]))
    summary.stats = {
        "file_count": len(sources),
        "uvm_file_count": uvm_file_count,
        "entity_counts": dict(entity_counter),
        "edge_count": len(summary.edges),
    }
    return summary


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


def write_summary(output_dir: Path, summary_name: str, summary: AnalysisSummary) -> Path:
    summary_path = output_dir / summary_name
    payload = {
        "stats": summary.stats,
        "entities": [asdict(entity) for entity in summary.entities],
        "edges": summary.edges,
        "files": summary.file_summaries,
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return summary_path


def mermaid_id(raw: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", raw)
    return f"n_{cleaned}" if not cleaned[:1].isalpha() else cleaned


def select_visual_nodes(summary: AnalysisSummary, limit: int = 24) -> list[str]:
    score: Counter[str] = Counter()
    for entity in summary.entities:
        score[entity.name] += 3
    for edge in summary.edges:
        score[edge["from"]] += 1
        score[edge["to"]] += 1
    return [name for name, _ in score.most_common(limit)]


def build_mermaid(summary: AnalysisSummary) -> str:
    chosen = set(select_visual_nodes(summary))
    lines = ["```mermaid", "graph TD"]
    declared: set[str] = set()

    def declare(node: str) -> None:
        node_id = mermaid_id(node)
        if node_id in declared:
            return
        declared.add(node_id)
        label = node.replace('"', "'")
        lines.append(f'    {node_id}["{label}"]')

    for edge in summary.edges:
        if edge["from"] not in chosen and edge["to"] not in chosen:
            continue
        declare(edge["from"])
        declare(edge["to"])
        lines.append(
            f"    {mermaid_id(edge['from'])} -->|{edge['type']}| {mermaid_id(edge['to'])}"
        )

    if len(lines) == 2:
        lines.append("    empty[\"No heuristic edges recovered\"]")
    lines.append("```")
    return "\n".join(lines)


def write_visualization(output_dir: Path, visualization_name: str, manifest_path: Path, summary: AnalysisSummary) -> Path:
    graph_path = output_dir / visualization_name
    stats = summary.stats
    top_files = sorted(summary.file_summaries, key=lambda item: int(item["line_count"]), reverse=True)[:10]
    lines = [
        "# Graphify Structural Visualization",
        "",
        f"Manifest: `{manifest_path.name}`",
        "",
        "## Snapshot",
        "",
        f"- Files: {stats.get('file_count', 0)}",
        f"- UVM-related files: {stats.get('uvm_file_count', 0)}",
        f"- Entities: {sum(summary.stats.get('entity_counts', {}).values())}",
        f"- Heuristic edges: {stats.get('edge_count', 0)}",
        "",
        "## Mermaid overview",
        "",
        build_mermaid(summary),
        "",
        "## Largest files",
        "",
        "| File | Lines | UVM | run_test | config_db | analysis_port |",
        "| --- | ---: | :---: | :---: | :---: | :---: |",
    ]
    for item in top_files:
        lines.append(
            f"| `{item['file']}` | {item['line_count']} | {'Y' if item['has_uvm'] else 'N'} | {'Y' if item['has_run_test'] else 'N'} | {'Y' if item['has_config_db'] else 'N'} | {'Y' if item['has_analysis_port'] else 'N'} |"
        )
    lines.extend([
        "",
        "## Notes",
        "",
        "- This view is derived from deterministic source scanning, so it remains available even without a Graphify install.",
        "- Use it as a reviewable baseline, then compare against richer Graphify graph exports when available.",
    ])
    graph_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return graph_path


def resolve_python_for_renderers() -> str:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "venv" / "bin" / "python"
        if candidate.exists():
            return str(candidate)
    return sys.executable


def render_additional_artifacts(summary_path: Path) -> list[Path]:
    scripts_dir = Path(__file__).resolve().parent
    python_bin = resolve_python_for_renderers()
    render_jobs = [
        (scripts_dir / "render_graphify_html.py", summary_path.parent / "network-graph.html"),
        (scripts_dir / "render_graphify_network_png.py", summary_path.parent / "network-graph.png"),
        (scripts_dir / "render_graphify_summary_png.py", summary_path.parent / "graph-report.png"),
    ]
    written: list[Path] = []
    for renderer, output_path in render_jobs:
        completed = subprocess.run(
            [python_bin, str(renderer), str(summary_path), "--output", str(output_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.strip()
            print(
                f"ARTIFACT_RENDER_FAILED: {output_path.name}: {stderr or f'return code {completed.returncode}'}",
                file=sys.stderr,
            )
            continue
        written.append(output_path)
    return written


def run_graphify(graphify_bin: str, manifest_path: Path, output_dir: Path, passthrough: list[str]) -> int:
    resolved = shutil.which(graphify_bin) if not Path(graphify_bin).exists() else graphify_bin
    if not resolved:
        print(
            "GRAPHIFY_NOT_FOUND: manifest/summary/visualization written, but Graphify CLI is unavailable.",
            file=sys.stderr,
        )
        return 2

    command = [resolved, "analyze", "--manifest", str(manifest_path), "--output-dir", str(output_dir)]
    command.extend(passthrough)
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    args = parse_args()
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
    summary = analyze_sources(input_root, sources)
    summary_path = write_summary(output_dir, args.summary_name, summary)
    visualization_path = write_visualization(output_dir, args.visualization_name, manifest_path, summary)
    extra_artifacts = render_additional_artifacts(summary_path)

    print(f"MANIFEST_WRITTEN: {manifest_path}")
    print(f"SUMMARY_WRITTEN: {summary_path}")
    print(f"VISUALIZATION_WRITTEN: {visualization_path}")
    for artifact in extra_artifacts:
        print(f"ARTIFACT_WRITTEN: {artifact}")
    print(f"SOURCE_COUNT: {len(sources)}")

    if args.manifest_only:
        return 0

    return run_graphify(args.graphify_bin, manifest_path, output_dir, args.graphify_args)


if __name__ == "__main__":
    raise SystemExit(main())
