# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/.cache/graphify_repos/ibex-master/rtl  (2026-05-02)

## Corpus Check
- 30 files · ~73,952 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 33 nodes · 22 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]

## God Nodes (most connected - your core abstractions)
1. `ibex_pkg` - 20 edges
2. `ibex_tracer_pkg` - 1 edges
3. `prim_secded_pkg` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (1): ibex_pkg

### Community 1 - "Community 1"
Cohesion: 1.0
Nodes (1): ibex_tracer_pkg

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (1): prim_secded_pkg

## Knowledge Gaps
- **2 isolated node(s):** `ibex_tracer_pkg`, `prim_secded_pkg`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 0`** (20 nodes): `ibex_alu.sv`, `ibex_branch_predict.sv`, `ibex_compressed_decoder.sv`, `ibex_controller.sv`, `ibex_core.sv`, `ibex_cs_registers.sv`, `ibex_decoder.sv`, `ibex_dummy_instr.sv`, `ibex_ex_block.sv`, `ibex_icache.sv`, `ibex_id_stage.sv`, `ibex_if_stage.sv`, `ibex_multdiv_fast.sv`, `ibex_multdiv_slow.sv`, `ibex_pkg`, `ibex_pmp.sv`, `ibex_top.sv`, `ibex_top_tracing.sv`, `ibex_tracer_pkg.sv`, `ibex_wb_stage.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 1`** (2 nodes): `ibex_tracer_pkg`, `ibex_tracer.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 2`** (2 nodes): `ibex_lockstep.sv`, `prim_secded_pkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ibex_pkg` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.421) - this node is a cross-community bridge._
- **What connects `ibex_tracer_pkg`, `prim_secded_pkg` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._