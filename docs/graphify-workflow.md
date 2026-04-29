# Graphify Workflow

This repository now has a minimal, reproducible entrypoint for Graphify-based source analysis.

## What it does

`scripts/run_graphify.py`:

- scans an input directory for Verilog/SystemVerilog sources
- writes a stable JSON manifest under `graph/graphify_outputs/`
- optionally invokes a `graphify analyze` CLI if Graphify is installed

This keeps the repository usable even when Graphify setup differs across machines.

## Quick start

Write a manifest only:

```bash
python3 scripts/run_graphify.py examples/rtl --manifest-only
```

Analyze the UVM example when Graphify is installed:

```bash
python3 scripts/run_graphify.py examples/uvm_tb
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
└── ... Graphify-generated outputs ...
```

`sources.json` records:

- absolute input root
- source count
- absolute source paths in deterministic order

## Why this comes first

Before agents can review RTL or UVM structure, the project needs one repeatable way to define analysis inputs. The manifest gives us that contract.
