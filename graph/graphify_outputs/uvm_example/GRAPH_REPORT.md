# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/examples/uvm_tb  (2026-05-02)

## Corpus Check
- Corpus is ~739 words - fits in a single context window. You may not need a graph.

## Summary
- 5 nodes · 3 edges · 2 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]

## God Nodes (most connected - your core abstractions)
1. `uvm_pkg` - 2 edges
2. `tb_counter_pkg` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 1.0
Nodes (1): tb_counter_pkg

### Community 1 - "Community 1"
Cohesion: 1.0
Nodes (1): uvm_pkg

## Knowledge Gaps
- **1 isolated node(s):** `tb_counter_pkg`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 0`** (2 nodes): `tb_counter_pkg`, `tb_counter_uvm.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 1`** (2 nodes): `tb_counter_pkg.sv`, `uvm_pkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `uvm_pkg` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.333) - this node is a cross-community bridge._
- **What connects `tb_counter_pkg` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._