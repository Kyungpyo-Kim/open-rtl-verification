# Graphify Workflow

This repository now has a reproducible Graphify entrypoint that works for both local examples and larger open-source RTL/UVM repositories.

## What it does

`scripts/run_graphify.py`:

- scans a local input directory or stages a remote git repository
- optionally honors simulator-style filelists for ordering and exact source selection
- writes a stable JSON manifest under `graph/graphify_outputs/`
- emits a heuristic `summary.json` plus Markdown, HTML, and PNG visualizations
- optionally invokes a `graphify analyze` CLI if Graphify is installed

This keeps the repository usable even when Graphify setup differs across machines.

## Quick start

Write manifest, summary, and visualization only:

```bash
python3 scripts/run_graphify.py examples/rtl --manifest-only
```

Analyze the UVM example when Graphify is installed:

```bash
python3 scripts/run_graphify.py examples/uvm_tb
```

Analyze a larger public RTL target with sparse checkout:

```bash
python3 scripts/run_graphify.py \
  https://github.com/lowRISC/ibex.git \
  --repo-ref master \
  --sparse-path rtl \
  --output-dir graph/graphify_outputs/ibex_rtl \
  --manifest-only
```

Pass through extra CLI options to Graphify:

```bash
python3 scripts/run_graphify.py examples/uvm_tb --graphify-args --format json
```

## Output layout

Default output directory:

```text
graph/graphify_outputs/latest/
├── sources.json
├── summary.json
├── graph.md
├── network-graph.html
├── network-graph.png
├── graph-report.png
└── ... Graphify-generated outputs ...
```

`sources.json` records:

- absolute input root
- source count
- absolute source paths in deterministic order

`summary.json` adds a lightweight structural inventory:

- recovered modules, interfaces, packages, and classes
- import / inheritance / instantiation edges
- per-file UVM markers such as `run_test`, `uvm_config_db`, and analysis-port usage

`graph.md` renders that inventory as Markdown with a Mermaid graph and a largest-file table.

## Next reading

- `docs/graphify-open-targets.md` for larger open RTL/UVM target runs
- `configs/open_targets.json` for reusable public target presets
