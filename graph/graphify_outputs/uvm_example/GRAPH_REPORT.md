# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/examples/uvm_tb  (2026-05-02)

## Corpus Check
- 3 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 11 nodes · 9 edges · 2 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]

## God Nodes (most connected - your core abstractions)
1. `tb_counter_uvm` - 5 edges
2. `uvm_pkg` - 2 edges
3. `body` - 1 edges
4. `tb_counter_pkg` - 1 edges
5. `counter_if` - 1 edges
6. `counter` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.4
Nodes (2): body, uvm_pkg

### Community 1 - "Community 1"
Cohesion: 0.4
Nodes (4): counter, counter_if, tb_counter_pkg, tb_counter_uvm

## Knowledge Gaps
- **4 isolated node(s):** `body`, `tb_counter_pkg`, `counter_if`, `counter`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 0`** (5 nodes): `body`, `build_phase()`, `connect_phase()`, `tb_counter_pkg.sv`, `uvm_pkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tb_counter_uvm` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.578) - this node is a cross-community bridge._
- **Why does `uvm_pkg` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.444) - this node is a cross-community bridge._
- **What connects `body`, `tb_counter_pkg`, `counter_if` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._