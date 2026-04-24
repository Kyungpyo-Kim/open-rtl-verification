# Open RTL Verification

> 100% open-source AI-agent framework for RTL verification.

## Overview

Open RTL Verification is an open-source framework for exploring how AI agents can assist, automate, and improve RTL verification workflows.

The project focuses on Verilog/SystemVerilog RTL and testbench analysis, starting with graph-based code understanding using Graphify. The long-term goal is to build an agentic verification framework that can analyze RTL, understand testbenches, generate verification plans, suggest assertions, create tests, run simulations, and summarize coverage gaps.

## Goals

### Short-term Goal

Use Graphify to analyze RTL and testbench repositories.

Initial targets:

- Parse RTL and testbench structure
- Build a knowledge graph of modules, interfaces, signals, tasks, classes, and dependencies
- Identify verification-relevant relationships
- Summarize DUT and TB architecture
- Help engineers understand unfamiliar RTL/TB codebases faster

### Long-term Goal

Develop an AI-agent-based RTL verification framework.

The framework should eventually support:

- RTL design understanding
- Testbench structure analysis
- Verification plan generation
- Assertion suggestion
- Test scenario generation
- Coverage gap analysis
- Regression result summarization
- Bug hypothesis generation
- Debug assistance from logs, waveforms, traces, and failing seeds

## Why This Project?

RTL verification is expensive, repetitive, and highly dependent on expert knowledge.

Modern AI agents can help with:

- Codebase exploration
- Design intent extraction
- Verification checklist generation
- Testbench review
- Assertion and coverage suggestion
- Debug log summarization
- Regression triage

However, RTL verification has strict correctness requirements. This project is not about replacing verification engineers. It is about building open, inspectable, reproducible tools that help engineers verify RTL more effectively.

## Core Principles

- 100% open source
- Verilog/SystemVerilog-first
- Compatible with open-source RTL projects
- Toolchain-friendly
- Human-in-the-loop by default
- Reproducible experiments
- Transparent AI-agent reasoning outputs
- No vendor lock-in
- Designed for real verification workflows

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
RTL / TB source
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
│   └── tb/
├── graph/
│   ├── graphify_outputs/
│   └── queries/
├── agents/
│   ├── rtl_analyzer/
│   ├── tb_analyzer/
│   ├── verification_planner/
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
- SymbiYosys
- Yosys
- Surelog/UHDM

## Example Use Cases

### 1. RTL Structure Analysis

```bash
open-rtl verify analyze-rtl ./examples/rtl
```

### 2. Testbench Analysis

```bash
open-rtl verify analyze-tb ./examples/tb
```

### 3. Verification Plan Draft

```bash
open-rtl verify plan ./examples/rtl ./examples/tb
```

## Roadmap

### Phase 0: Project Bootstrap

- [ ] Define project structure
- [ ] Add example RTL/TB projects
- [ ] Add Graphify-based analysis workflow
- [ ] Document experiment process

### Phase 1: Graph-Based RTL/TB Understanding

- [ ] Generate repository knowledge graph
- [ ] Extract RTL module hierarchy
- [ ] Extract TB component relationships
- [ ] Add graph query examples
- [ ] Generate human-readable summaries

### Phase 2: Agent-Assisted Verification Planning

- [ ] Generate verification plan drafts
- [ ] Suggest directed tests
- [ ] Suggest assertions
- [ ] Suggest functional coverage points

### Phase 3: Simulation Integration

- [ ] Integrate Verilator
- [ ] Integrate Icarus Verilog
- [ ] Integrate cocotb
- [ ] Add regression runner

### Phase 4: Debug and Regression Triage

- [ ] Parse simulation logs
- [ ] Summarize failing tests
- [ ] Generate debug hypotheses

### Phase 5: Formal and Assertion Flow

- [ ] Generate SVA candidates
- [ ] Integrate SymbiYosys
- [ ] Run formal checks

## Evaluation Strategy

- RTL structure understanding accuracy
- Testbench understanding accuracy
- Verification plan usefulness
- Assertion quality
- Coverage gap detection
- Debug efficiency improvement

## License

Apache License 2.0

## Project Status

Early concept stage.

Focus:

Analyze RTL and testbench repositories with Graphify and convert results into verification insights.
