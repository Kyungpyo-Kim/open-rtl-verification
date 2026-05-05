# Graphify Workflow

This repository keeps the Graphify entrypoint intentionally small and reproducible.

## What it does

`scripts/run_graphify.py`:

- scans a local input directory or stages a remote git repository
- optionally honors simulator-style filelists for ordering and exact source selection
- writes a stable JSON manifest under `graph/graphify_outputs/`
- uses the official `graphifyy` Python package to generate `graph.json`, `graph.html`, and `GRAPH_REPORT.md`

The repository does not maintain a custom heuristic parser, summary format, or bespoke graph renderer anymore. Artifact structure follows Graphify's native outputs, with PNG capture kept as a small debugging helper.

## Quick start

### Default, upstream package install

```bash
python3 -m pip install --user graphifyy
graphify install --platform claw
```

### Local fork development via submodule

This repository can pin a Graphify fork as a git submodule for local extractor work.

```bash
git submodule update --init --recursive
python3 -m pip install --user -e ./vendor/graphify
graphify install --platform claw
```

`scripts/run_graphify.py` now prefers the vendored fork automatically when `vendor/graphify/` exists. You can still override it explicitly:

```bash
python3 scripts/run_graphify.py examples/rtl --graphify-source vendor
python3 scripts/run_graphify.py examples/rtl --graphify-source installed
```

Each run prints `GRAPHIFY_SOURCE: vendor` or `GRAPHIFY_SOURCE: installed` so the active import path is visible.

Write the manifest only:

```bash
python3 scripts/run_graphify.py examples/rtl --manifest-only
```

Generate Graphify artifacts for the UVM example:

```bash
python3 scripts/run_graphify.py examples/uvm_tb
```

Analyze a larger public RTL target with sparse checkout:

```bash
python3 scripts/run_graphify.py \
  https://github.com/lowRISC/ibex.git \
  --repo-ref master \
  --sparse-path rtl \
  --output-dir graph/graphify_outputs/ibex_rtl
```

## Output layout

Default output directory after a full run:

```text
graph/graphify_outputs/latest/
├── sources.json
├── graph.json
├── graph.html
└── GRAPH_REPORT.md
```

`sources.json` records:

- absolute input root
- source count
- absolute source paths in deterministic order
- relative source paths
- optional repo and filelist metadata

## Debugging support

If Graphify emits HTML artifacts and you want a static screenshot for review, use:

```bash
python3 scripts/render_html_to_png.py path/to/graphify-output.html --output path/to/graphify-output.png
```

This is a lightweight debugging helper only, not part of the main workflow. If Chromium is not installed system-wide, a Playwright-managed browser under `~/.cache/ms-playwright/` is also supported.

## Next reading

- `docs/graphify-open-targets.md` for larger open RTL/UVM target runs
- `configs/open_targets.json` for reusable public target presets
