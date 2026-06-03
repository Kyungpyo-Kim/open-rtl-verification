# Open RTL Verification

> 100% open-source AI-agent framework for RTL verification.

## Overview

Open RTL Verification is an open-source framework for exploring how AI agents can assist, automate, and improve RTL verification workflows.

The project focuses on Verilog/SystemVerilog RTL and testbench analysis, including both lightweight SystemVerilog testbenches and UVM-based verification environments, starting with graph-based code understanding using Graphify. The long-term goal is to build an agentic verification framework that can analyze RTL, understand testbenches, generate verification plans, suggest assertions, create tests, run simulations, and summarize coverage gaps.

## Goals

### Short-term Goal

Use Graphify to analyze RTL and testbench repositories.

Initial targets:

- Parse RTL and testbench structure
- Build a knowledge graph of modules, interfaces, signals, tasks, classes, UVM components, sequences, TLM connections, and dependencies
- Identify verification-relevant relationships
- Summarize DUT, TB, and UVM environment architecture
- Detect likely UVM integration risks such as config mismatches, virtual interface binding issues, clock/reset alignment problems, and broken connectivity paths
- Help engineers understand unfamiliar RTL/TB codebases faster

### Long-term Goal

Develop an AI-agent-based RTL verification framework.

The framework should eventually support:

- RTL design understanding
- Testbench structure analysis
- UVM environment and sequence analysis
- UVM integration risk analysis (config_db, virtual interface binding, clock/reset alignment, agent connectivity)
- Verification plan generation
- Assertion suggestion
- Test scenario generation
- Functional coverage gap analysis
- Regression result summarization
- CSR / register-spec-driven verification review
- Bug hypothesis generation
- Debug assistance from logs, waveforms, traces, and failing seeds

## Why This Project?

RTL verification is expensive, repetitive, and highly dependent on expert knowledge.

Modern AI agents can help with:

- Codebase exploration
- Design intent extraction
- Verification checklist generation
- Testbench and UVM environment review
- Assertion and coverage suggestion
- Sequence and stimulus review
- Debug log summarization
- Regression triage
- UVM connectivity and integration sanity checks
- CSR / RAL consistency review

However, RTL verification has strict correctness requirements. This project is not about replacing verification engineers. It is about building open, inspectable, reproducible tools that help engineers verify RTL more effectively.

## Safe AI Adoption Scope

This project prioritizes bounded, inspectable AI assistance over fully autonomous verification.

### Strong early-fit AI tasks

- Testbench skeleton and structure review
- Assertion draft generation with human review
- Coverage hole clustering and intent summarization
- Regression failure summarization and triage
- UVM connectivity sanity check
- Spec-derived verification checklist review
- CSR / register model consistency review

### Explicit non-goals for early phases

- Fully autonomous sign-off decisions
- Unchecked stimulus generation for production regressions
- Replacing verification engineer judgment
- Opaque black-box reasoning without traceable evidence

## Core Principles

- 100% open source
- Verilog/SystemVerilog-first
- UVM-aware verification workflow
- Compatible with open-source RTL projects
- Toolchain-friendly
- Human-in-the-loop by default
- Reproducible experiments
- Transparent AI-agent reasoning outputs
- No vendor lock-in
- Designed for real verification workflows
- Bounded AI assistance before autonomous action
- Extend/wrap third-party VIP rather than modifying it directly

## Target Users

- RTL verification engineers
- Digital design engineers
- Open-source hardware contributors
- Students learning hardware verification
- Researchers exploring AI for EDA
- Developers building agentic engineering tools

## Initial Scope

The first milestone focuses on static analysis.

```
RTL / SV TB / UVM source
         |
         v
   Graphify analysis
         |
         v
Design + verification knowledge graph
         |
         v
AI-agent assisted review
         |
         v
 Verification insights
```

## Planned Architecture

```
open-rtl-verification/
├── examples/
│   ├── rtl/
│   ├── tb/
│   └── uvm_tb/
├── graph/
│   ├── graphify_outputs/
│   └── queries/
├── agents/
│   ├── rtl_analyzer/
│   ├── tb_analyzer/
│   ├── uvm_analyzer/
│   ├── uvm_integration_reviewer/
│   ├── verification_planner/
│   ├── csr_spec_reviewer/
│   └── regression_summarizer/
├── scripts/
├── docs/
├── tests/
└── README.md
```

## Candidate Toolchain

- Graphify
- Verilator
- Icarus Verilog
- cocotb
- UVM (with simulator support where applicable)
- SymbiYosys
- Yosys
- Surelog/UHDM

## Example Use Cases

### 1. RTL Structure Analysis

```bash
python3 scripts/run_graphify.py examples/rtl --manifest-only
```

Install Graphify first:

```bash
python3 -m pip install --user graphifyy
graphify install --platform claw
```

If you want to modify Graphify locally, use the pinned submodule fork instead:

```bash
git submodule update --init --recursive
python3 -m pip install --user -e ./vendor/graphify
graphify install --platform claw
```

Then generate Graphify artifacts directly:

```bash
python3 scripts/run_graphify.py examples/rtl
```

The workflow now also supports:

- public git repo staging for open RTL / UVM targets
- sparse checkout for large repositories
- filelist-aware source selection, including nested `-F` filelists
- deterministic `sources.json` manifest generation for Graphify
- named open-target presets from `configs/open_targets.json`
- explicit Graphify source selection via `--graphify-source {auto,vendor,installed}`

Preset-driven example:

```bash
python3 scripts/run_graphify.py --target ibex_rtl --manifest-only
```

Example, larger open RTL target:

```bash
python3 scripts/run_graphify.py \
  https://github.com/lowRISC/ibex.git \
  --repo-ref master \
  --sparse-path rtl \
  --output-dir graph/graphify_outputs/ibex_rtl
```

Example, UVM filelist-driven manifest generation with nested `-F` support:

```bash
python3 scripts/run_graphify.py \
  examples/uvm_tb \
  --filelist files.f \
  --manifest-only \
  --graphify-source vendor \
  --output-dir graph/graphify_outputs/uvm_manifest
```

### 2. Testbench Analysis

```bash
open-rtl verify analyze-tb ./examples/tb
```

### 3. UVM Environment Analysis

```bash
open-rtl verify analyze-uvm ./examples/uvm_tb
```

Expected analysis targets:
- UVM component hierarchy
- factory usage and overrides
- sequence/sequencer flow
- config_db propagation paths
- virtual interface binding points
- agent active/passive mode
- scoreboard / monitor / predictor connectivity
- clock/reset distribution assumptions

### 4. UVM Integration Review

```bash
open-rtl verify review-uvm-integration ./examples/uvm_tb
```

Review focus:
- config mismatch risks
- clock/reset alignment issues
- broken TLM or analysis connections
- duplicated or missing checking responsibility
- VIP integration boundary issues

### 5. Verification Plan Draft

```bash
open-rtl verify plan ./examples/rtl ./examples/tb
```

## Testing

Run the test suite from the repository root:

```bash
python3 -m pytest tests/ -v
```

All tests are expected to pass. When adding new features, please include corresponding test cases in the `tests/` directory.

## Verification Review Principles

### UVM integration analysis first

The project should treat many verification bottlenecks as integration problems rather than framework problems. High-value analysis targets include:

- config_db path mismatches
- virtual interface binding gaps
- clock/reset alignment assumptions
- agent configuration inconsistencies
- missing or duplicated checking responsibility across monitors, scoreboards, and predictors

### Spec-driven verification support

The project should support spec-derived verification review, especially for CSR and hardware/software interface flows.

Target outcomes:
- ingest register or CSR specifications
- compare intent against register models and access behavior
- derive verification checklist items for human review
- identify likely reset/access-policy mismatches early

### VIP handling philosophy

When third-party VIP is present, the preferred workflow is:

- extend VIP
- wrap VIP
- configure VIP
- do not modify vendor or third-party VIP directly unless there is no alternative

This keeps reuse, upgrades, and regression stability manageable.

## Roadmap

### Phase 0: Project Bootstrap

- [x] Define project structure
- [x] Add example RTL/TB projects
- [x] Add example UVM environment
- [x] Add Graphify-based analysis workflow
- [ ] Document experiment process
- [ ] Define documentation for safe AI adoption boundaries
- [ ] Add minimal VIP integration review checklist

### Phase 1: Graph-Based RTL/TB Understanding

- [ ] Generate repository knowledge graph
- [ ] Extract RTL module hierarchy
- [ ] Extract TB component relationships
- [ ] Extract UVM component hierarchy, factory usage, and sequence flow
- [ ] Trace config_db propagation and virtual interface bindings
- [ ] Detect scoreboard / monitor / predictor connectivity structure
- [ ] Flag clock/reset topology assumptions visible from code
- [ ] Add graph query examples
- [ ] Generate human-readable summaries

### Phase 2: Agent-Assisted Verification Planning

- [ ] Generate verification plan drafts
- [ ] Suggest directed tests
- [ ] Suggest UVM sequence scenarios
- [ ] Suggest assertions
- [ ] Suggest functional coverage points
- [ ] Generate UVM integration review findings with evidence
- [ ] Review CSR / register spec against RAL and access behavior
- [ ] Generate spec-derived verification checklists for human review

### Phase 3: Simulation Integration

- [ ] Integrate Verilator
- [ ] Integrate Icarus Verilog
- [ ] Integrate cocotb
- [ ] Define UVM-capable simulation flow
- [ ] Add regression runner
- [ ] Add bounded AI hooks for regression triage and coverage review

### Phase 4: Debug and Regression Triage

- [ ] Parse simulation logs
- [ ] Summarize failing tests
- [ ] Cluster failures by likely root cause
- [ ] Generate debug hypotheses

### Phase 5: Formal and Assertion Flow

- [ ] Generate SVA candidates
- [ ] Integrate SymbiYosys
- [ ] Run formal checks
- [ ] Connect structural findings to assertion and safety-property drafts

## Evaluation Strategy

- RTL structure understanding accuracy
- Testbench understanding accuracy
- UVM environment understanding accuracy
- UVM integration issue detection precision
- Verification plan usefulness
- Assertion quality
- Coverage gap detection
- CSR / RAL consistency review usefulness
- Debug efficiency improvement

## License

Apache License 2.0

## Project Status

Early concept stage.

Current repository assets:

- `examples/rtl/counter.sv`: small DUT for graph extraction experiments
- `examples/tb/tb_counter.sv`: matching SystemVerilog testbench skeleton
- `examples/uvm_tb/`: minimal UVM environment for structure, sequence, analysis-port connectivity, and virtual-interface binding experiments
- `scripts/run_graphify.py`: Graphify entrypoint with repo staging, sparse checkout, filelist support, and manifest generation
- `configs/open_targets.json`: reusable open-source target presets for larger RTL/UVM analysis
- `docs/graphify-workflow.md`: workflow usage notes
- `docs/graphify-open-targets.md`: larger open-target manifest examples

Focus:

Analyze RTL, testbench, and UVM repositories with Graphify and convert results into verification insights.

Near-term emphasis:

- Help engineers understand UVM environments faster
- Surface integration risks before simulation debug burns time
- Review CSR / register-driven verification intent against implementation artifacts
- Keep AI outputs reviewable, bounded, and traceable

## Current Graphify TODOs

- [x] Vendor Graphify fork as a submodule at `vendor/graphify`
- [x] Recover basic SystemVerilog module hierarchy edges (`defines`, `instantiates`) from tree-sitter field mismatches
- [x] Recover missing instantiations in parser-error and generate-heavy regions
- [x] Tighten fallback precision with comment masking, statement-shaped parsing, module-name validation, and keyword rejection
- [x] Remove project-specific `prim_` promotion from the fallback structural extractor and replace it with a generalized unresolved-external relation
- [x] Make `scripts/run_graphify.py` prefer the vendored Graphify fork by default so local extractor work actually shows up in generated artifacts
- [x] Re-run Ibex targets after extractor improvements and compare edge coverage deltas

## Graphify Extractor Next Backlog

- [x] Preserve repeated instantiations as weighted edges in the final graph
- [x] Add signal connectivity extraction, starting with instance port bindings, simple `assign` dependencies, and basic procedural assignments
- [x] Add function/task call edges for local helper-heavy RTL modules
- [x] Add package-qualified symbol/type usage edges such as `ibex_pkg::...`
- [ ] Add UVM-oriented extraction adapters on top of the same confidence/scoping framework

Current call-edge, package-symbol, and basic signal-connectivity coverage is validated by `tests/test_graphify_verilog_calls.py` for local helper functions, task-to-function calls, package-qualified symbol/type uses, named and positional instance port bindings, simple `assign` dependencies, and basic procedural assignments including condition-gated dependencies without declaration noise.

Recent Graphify application summary:

- validated on local UVM example manifest generation
- applied to `lowRISC/ibex` RTL hierarchy
- applied to `lowRISC/opentitan` UART DV slice plus shared UVM infrastructure
- kept README concise, with detailed target notes moved to `docs/graphify-open-targets.md`
