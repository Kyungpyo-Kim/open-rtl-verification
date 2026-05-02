# Graphify Extractor Stabilization

This note captures the extractor work completed during the Ibex graph cleanup, why it was needed, what was fixed, and what remains as backlog.

## Scope

This stabilization pass focused on one bounded goal:

- make SystemVerilog structural edge extraction reliable enough for RTL hierarchy graphs
- remove false hubs caused by fallback parsing noise
- ensure local Graphify extractor edits are reflected in generated artifacts

This pass does **not** attempt to solve all future semantic edges such as dataflow, function calls, or UVM-specific relations.

## Problem Summary

During Ibex graph generation, the original fallback extraction path produced major false positives:

- parser-error and generate-heavy files missed real `instantiates` edges
- loose regex fallback misread non-instantiation text as module instances
- `ibex_tracer.sv` became a giant false hub because instruction case labels such as `INSN_ADD` were treated as instantiated modules
- the project could regenerate artifacts with the installed Graphify package instead of the vendored fork, hiding local extractor fixes

## Stabilization Checklist

### Done in this pass

- [x] Recover missing `instantiates` edges when tree-sitter reports parse errors
- [x] Restrict fallback extraction to precision-first statement parsing instead of loose multiline regex matches
- [x] Mask comments and string literals before fallback parsing so prose and macros do not become graph nodes
- [x] Reject obvious non-module tokens and labels such as `default`, `begin`, `endcase`, `unique`, and similar control words
- [x] Cross-check fallback module candidates against known local `module`/`macromodule` definitions when possible
- [x] Keep likely external primitive cells only through conservative heuristics (`prim_*`, escaped identifiers, ALL_CAPS cells)
- [x] Dedupe structural `instantiates` edges emitted from mixed AST + fallback paths
- [x] Make `scripts/run_graphify.py` prefer the vendored `vendor/graphify` fork by default
- [x] Re-run Ibex extraction with the vendored fork and verify the false-hub issue is gone
- [x] Document results, known limits, and next backlog clearly

### Validation results from this pass

- [x] `ibex_tracer.sv` fake `instantiates` edges removed (`188 -> 0`)
- [x] Ibex graph regenerated with vendored Graphify
- [x] High-resolution PNG regenerated after the extractor fix

Current generated-artifact snapshot after the vendored rerun:

- `GRAPHIFY_SOURCE: vendor`
- `graph/graphify_outputs/ibex_rtl/graph.json`
  - `155 nodes`
  - `151 links`
  - relations: `defines=28`, `imports_from=22`, `contains=63`, `instantiates=38`
  - `ibex_tracer instantiates edges = 0`

## Code Changes

### 1. `vendor/graphify/graphify/extract.py`

Structural extractor changes:

- added safer fallback parsing for `module instantiation` recovery when tree-sitter reports errors
- masks comments and strings before fallback scanning
- scans semicolon-terminated statements instead of loose multiline chunks
- validates optional `#(...)` parameter blocks with balanced parentheses
- rejects control-flow labels and obvious non-module keywords
- validates module-type candidates against locally discoverable module definitions
- dedupes repeated AST/fallback structural edges cleanly

Design intent:

- prefer **precision over recall** for fallback edges
- treat fallback as recovery only, not as a free-form text mining pass

### 2. `scripts/run_graphify.py`

Pipeline changes:

- added `--graphify-source {auto,vendor,installed}`
- default `auto` now prefers `vendor/graphify` when present
- prints `GRAPHIFY_SOURCE:` during runs so the active import path is explicit

Design intent:

- prevent stale installed wheels from hiding local extractor work
- make validation runs reproducible and obvious

### 3. `README.md`

Project updates:

- moved completed stabilization tasks into checked items
- separated future extractor backlog from the finished stabilization pass

## Why the false hub happened

The key failure mode was not Ibex-specific. It is a general fallback-parser risk.

Bad pattern:

- parser sees syntax errors
- fallback scans text too loosely
- any identifier followed by `(` starts to look like a module instance
- case labels, opcode symbols, comments, and prose become fake `instantiates` edges

That is how `ibex_tracer` became a disconnected giant community even though it is mostly a helper-function and decode-logic module.

## Generalized Rule Going Forward

Fallback extraction must follow this rule:

> candidate first, validation second, final edge last

Meaning:

1. detect a possible edge candidate
2. validate it against syntax shape and symbol knowledge
3. emit the real edge only after validation passes

This rule should stay true even when future work adds:

- function-call edges
- package/type-use edges
- signal/dataflow edges
- UVM-specific structural relations

## Remaining Backlog

These are intentionally **not** part of the finished stabilization checklist above.

- [ ] Preserve repeated instantiations as multiedges or weighted edges
- [ ] Add function/task call extraction for helper-heavy RTL like `ibex_tracer`
- [ ] Add package-qualified symbol/type-use extraction
- [ ] Add signal connectivity edges such as instance port bindings and simple `assign` dependencies
- [ ] Add UVM-specific adapters using the same confidence and validation framework
- [ ] Split future graph views by confidence tier so exploratory edges do not pollute structural graphs

## Recommended Next Step

The next highest-value extractor task is:

1. function/task call edges

Why:

- it explains currently isolated helper-function communities
- it works for both RTL helper logic and UVM class/testbench code
- it fits the same candidate -> validation -> final-edge structure already introduced here
