# Graphify on Larger Open RTL and UVM Targets

This repository keeps checked-in open-target examples focused on Graphify inputs.

`run_graphify.py` can stage open git repositories, sparse-check out only the interesting RTL/UVM subtrees, honor filelists, and emit a deterministic manifest for Graphify.

## What changed

- local directory or remote git repo input
- sparse checkout support for large public repositories
- optional filelist-driven source selection
- deterministic `sources.json` manifest generation
- reusable open-target presets in `configs/open_targets.json`

## Recommended open targets

| Target | Type | Repo | Paths | Checked-in artifact |
| --- | --- | --- | --- | --- |
| `uvm_example` | Local UVM example | local repo | `examples/uvm_tb` via `files.f` | `sources.json`, `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `graph.png` |
| `ibex_rtl` | Large RTL hierarchy | `lowRISC/ibex` | `rtl` | `sources.json`, `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `graph.png` |
| `opentitan_uart_dv` | Large UVM/DV + IP RTL slice | `lowRISC/opentitan` | `hw/ip/uart`, `hw/dv/sv` | `sources.json`, `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `graph.png` |

These manifests and Graphify artifacts are checked in under `graph/graphify_outputs/` so runs stay reproducible even on machines where the source repos are not already staged.

## Example commands

### 0) Reuse a checked-in preset directly

```bash
python3 scripts/run_graphify.py --target ibex_rtl --manifest-only
```

Presets come from `configs/open_targets.json` and fill `repo_url`, `repo_ref`, sparse paths, and the default output directory. Explicit CLI flags still win.

### 1) Local UVM example with filelist ordering

```bash
python3 scripts/run_graphify.py \
  examples/uvm_tb \
  --filelist files.f \
  --output-dir graph/graphify_outputs/uvm_example
```

### 2) Larger open RTL target, Ibex

```bash
python3 scripts/run_graphify.py \
  https://github.com/lowRISC/ibex.git \
  --repo-ref master \
  --sparse-path rtl \
  --output-dir graph/graphify_outputs/ibex_rtl
```

### 3) Larger open UVM target, OpenTitan UART DV slice

```bash
python3 scripts/run_graphify.py \
  https://github.com/lowRISC/opentitan.git \
  --repo-ref master \
  --sparse-path hw/ip/uart \
  --sparse-path hw/dv/sv \
  --output-dir graph/graphify_outputs/opentitan_uart_dv
```

## Output files

Each checked-in example currently keeps:

```text
graph/graphify_outputs/<target>/
├── sources.json
├── graph.json
├── graph.html
├── GRAPH_REPORT.md
└── graph.png
```

`graph.png` is a debug screenshot captured from `graph.html` using `scripts/render_html_to_png.py`.

## Notes

The repository no longer ships a custom heuristic summary, Mermaid graph, or hand-rolled structural parser. The goal is to keep workflow ownership with Graphify itself and keep this repo limited to source collection, staging, Graphify invocation, and reproducible example artifacts.
