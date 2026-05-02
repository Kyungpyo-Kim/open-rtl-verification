# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/.cache/graphify_repos_fresh7/ibex-master  (2026-05-02)

## Corpus Check
- 30 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 148 nodes · 138 edges · 17 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]

## God Nodes (most connected - your core abstractions)
1. `ibex_tracer` - 43 edges
2. `ibex_pkg` - 20 edges
3. `ibex_compressed_decoder` - 15 edges
4. `ibex_core` - 9 edges
5. `ibex_top` - 7 edges
6. `ibex_if_stage` - 6 edges
7. `ibex_lockstep` - 6 edges
8. `ibex_pmp` - 6 edges
9. `ibex_cs_registers` - 5 edges
10. `ibex_id_stage` - 4 edges

## Surprising Connections (you probably didn't know these)
- `ibex_register_file_latch` --instantiates--> `prim_clock_gating`  [EXTRACTED]
  ibex_register_file_latch.sv → ibex_top.sv

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (2): ibex_tracer_pkg, ibex_tracer

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (14): ibex_alu, ibex_pkg, prim_lfsr, ibex_alu, ibex_branch_predict, ibex_controller, ibex_decoder, ibex_dummy_instr (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (1): ibex_compressed_decoder

### Community 3 - "Community 3"
Cohesion: 0.22
Nodes (8): ibex_cs_registers, ibex_ex_block, ibex_id_stage, ibex_if_stage, ibex_load_store_unit, ibex_pmp, ibex_wb_stage, ibex_core

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (5): ibex_lockstep, prim_buf, prim_clock_gating, ibex_register_file_latch, ibex_top

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (3): ibex_compressed_decoder, ibex_dummy_instr, ibex_if_stage

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): ibex_core, prim_clock_mux2, prim_flop, prim_secded_pkg, ibex_lockstep

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (3): ibex_counter, ibex_csr, ibex_cs_registers

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (3): ibex_controller, ibex_decoder, ibex_id_stage

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (3): ibex_top, ibex_tracer, ibex_top_tracing

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (2): ibex_fetch_fifo, ibex_prefetch_buffer

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): ibex_counter

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): ibex_csr

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): ibex_fetch_fifo

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): ibex_load_store_unit

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): ibex_register_file_ff

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): ibex_register_file_fpga

## Knowledge Gaps
- **31 isolated node(s):** `ibex_if_stage`, `ibex_id_stage`, `ibex_ex_block`, `ibex_load_store_unit`, `ibex_wb_stage` (+26 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 0`** (44 nodes): `ibex_tracer_pkg`, `ibex_tracer.sv`, `ibex_tracer`, `cm_reg_to_str()`, `decode_b_insn()`, `decode_cb_insn()`, `decode_cb_sr_insn()`, `decode_ci_caddi16sp_insn()`, `decode_ci_caddi_insn()`, `decode_ci_cli_insn()`, `decode_ci_clui_insn()`, `decode_ci_cslli_insn()`, `decode_ciw_insn()`, `decode_cj_insn()`, `decode_compressed_load_insn()`, `decode_compressed_store_insn()`, `decode_cr_insn()`, `decode_cs_insn()`, `decode_csr_insn()`, `decode_expanded_insn()`, `decode_fence()`, `decode_i_funnelshift_insn()`, `decode_i_insn()`, `decode_i_jalr_insn()`, `decode_i_shift_insn()`, `decode_j_insn()`, `decode_load_insn()`, `decode_mnemonic()`, `decode_r1_insn()`, `decode_r_cmixcmov_insn()`, `decode_r_funnelshift_insn()`, `decode_r_insn()`, `decode_store_insn()`, `decode_u_insn()`, `decode_Zc_cu_insn()`, `decode_Zc_load_insn()`, `decode_Zc_store_insn()`, `decode_Zcmp_cmmv_insn()`, `decode_Zcmp_cmpp_insn()`, `get_csr_name()`, `get_fence_description()`, `printbuffer_dumpline()`, `reg_addr_to_abi_str()`, `reg_addr_to_str()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 2`** (15 nodes): `ibex_compressed_decoder.sv`, `ibex_compressed_decoder`, `cm_mv_reg()`, `cm_mva01s()`, `cm_mvsa01()`, `cm_pop_load_reg()`, `cm_push_store_reg()`, `cm_ret_ra()`, `cm_rlist_init()`, `cm_rlist_top_reg()`, `cm_sp_addi()`, `cm_stack_adj()`, `cm_stack_adj_base()`, `cm_stack_adj_word()`, `cm_zero_a0()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (3 nodes): `ibex_fetch_fifo`, `ibex_prefetch_buffer.sv`, `ibex_prefetch_buffer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `ibex_counter.sv`, `ibex_counter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `ibex_csr.sv`, `ibex_csr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `ibex_fetch_fifo.sv`, `ibex_fetch_fifo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `ibex_load_store_unit.sv`, `ibex_load_store_unit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `ibex_register_file_ff.sv`, `ibex_register_file_ff`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `ibex_register_file_fpga.sv`, `ibex_register_file_fpga`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ibex_pkg` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.325) - this node is a cross-community bridge._
- **Why does `ibex_compressed_decoder` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ibex_core` (e.g. with `ibex_ex_block` and `ibex_load_store_unit`) actually correct?**
  _`ibex_core` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ibex_if_stage`, `ibex_id_stage`, `ibex_ex_block` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._