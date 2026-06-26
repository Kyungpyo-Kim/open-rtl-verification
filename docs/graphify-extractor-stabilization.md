# Graphify Extractor Stabilization

This note captures the extractor work completed during the Ibex graph cleanup, why it was needed, what was fixed, and what remains as backlog.

## Scope

This stabilization pass focused on one bounded goal:

- make SystemVerilog structural edge extraction reliable enough for RTL hierarchy graphs
- remove false hubs caused by fallback parsing noise
- ensure local Graphify extractor edits are reflected in generated artifacts

This pass does **not** attempt to solve all future semantic edges such as dataflow or UVM-specific relations. Function/task call extraction and package-qualified symbol usage extraction were added later and are tracked below.

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
- [x] Keep unresolved fallback targets out of structural `instantiates` unless they can be justified by local definition discovery
- [x] Downgrade unresolved external-looking fallback targets to a separate low-confidence relation instead of hard-coding project-specific prefixes
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
- emits unresolved external-looking fallback targets as `references_unresolved_module` instead of forcing them into `instantiates`
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

- [x] Preserve repeated instantiations as weighted edges in the final graph
- [x] Add function/task call extraction for helper-heavy RTL like `ibex_tracer`
- [x] Add package-qualified symbol/type-use extraction
- [x] Add signal connectivity edges such as instance port bindings and simple `assign` dependencies
- [x] Add basic UVM-specific adapters using the same confidence and validation framework
- [ ] Split future graph views by confidence tier so exploratory edges do not pollute structural graphs

Function/task call extraction, package-qualified symbol usage extraction, the first signal-connectivity pass, and the early UVM-adapter pass are now covered by the repository test suite in `tests/test_graphify_verilog_calls.py`, which checks local helper-function calls, task-to-function calls, parameterized-call handling, `ibex_pkg::...` symbol usage without import noise, named and positional instance port bindings, simple `assign` dependencies, condition-gated procedural dependencies, plus `uvm_config_db` access, TLM `connect`, `sequence.start`, and `run_test` flows.

## Recommended Next Step

The next highest-value extractor task is now:

1. extend signal connectivity beyond the basic pass, especially richer procedural/dataflow patterns

Why:

- the first pass now covers named and positional instance port bindings, simple `assign` dependencies, and basic procedural assignments
- early UVM adapters now cover core verification-structure hints, so the bigger remaining information gap is richer dataflow extraction
- broader procedural/dataflow coverage still matters for real verification context, especially condition-gated updates and more complex expressions
- the same precision-first validation approach should keep exploratory connectivity from polluting the structural graph
