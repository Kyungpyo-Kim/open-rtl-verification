# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/.cache/graphify_repos_fresh6/ibex-master  (2026-05-02)

## Corpus Check
- 30 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 155 nodes · 151 edges · 16 communities detected
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.7)
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

## God Nodes (most connected - your core abstractions)
1. `ibex_tracer` - 43 edges
2. `ibex_pkg` - 20 edges
3. `ibex_compressed_decoder` - 15 edges
4. `ibex_core` - 12 edges
5. `ibex_top` - 10 edges
6. `ibex_if_stage` - 8 edges
7. `ibex_lockstep` - 7 edges
8. `ibex_pmp` - 6 edges
9. `ibex_cs_registers` - 5 edges
10. `prim_buf` - 4 edges

## Surprising Connections (you probably didn't know these)
- `ibex_core` --instantiates--> `prim_buf`  [INFERRED]
  ibex_core.sv → ibex_top.sv
- `ibex_core` --instantiates--> `prim_secded_inv_39_32_dec`  [INFERRED]
  ibex_core.sv → ibex_top.sv
- `ibex_if_stage` --instantiates--> `prim_buf`  [INFERRED]
  ibex_if_stage.sv → ibex_top.sv
- `ibex_load_store_unit` --instantiates--> `prim_buf`  [INFERRED]
  ibex_load_store_unit.sv → ibex_top.sv
- `ibex_if_stage` --instantiates--> `prim_secded_inv_39_32_dec`  [INFERRED]
  ibex_if_stage.sv → ibex_top.sv

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (2): ibex_tracer_pkg, ibex_tracer

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (15): ibex_alu, ibex_controller, ibex_decoder, ibex_pkg, prim_lfsr, ibex_alu, ibex_branch_predict, ibex_controller (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (15): ibex_compressed_decoder, ibex_cs_registers, ibex_dummy_instr, ibex_ex_block, ibex_id_stage, ibex_if_stage, ibex_load_store_unit, ibex_pmp (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (1): ibex_compressed_decoder

### Community 4 - "Community 4"
Cohesion: 0.2
Nodes (6): ibex_lockstep, prim_clock_gating, prim_ram_1p, prim_ram_1p_scr, ibex_register_file_latch, ibex_top

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (6): ibex_core, prim_clock_mux2, prim_count, prim_flop, prim_secded_pkg, ibex_lockstep

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (1): ibex_pmp

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (3): ibex_counter, ibex_csr, ibex_cs_registers

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (3): prim_secded_inv_28_22_dec, prim_secded_inv_28_22_enc, ibex_icache

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
Nodes (1): ibex_register_file_ff

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): ibex_register_file_fpga

## Knowledge Gaps
- **35 isolated node(s):** `ibex_if_stage`, `ibex_id_stage`, `ibex_ex_block`, `ibex_load_store_unit`, `ibex_wb_stage` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 0`** (44 nodes): `ibex_tracer_pkg`, `ibex_tracer.sv`, `ibex_tracer`, `cm_reg_to_str()`, `decode_b_insn()`, `decode_cb_insn()`, `decode_cb_sr_insn()`, `decode_ci_caddi16sp_insn()`, `decode_ci_caddi_insn()`, `decode_ci_cli_insn()`, `decode_ci_clui_insn()`, `decode_ci_cslli_insn()`, `decode_ciw_insn()`, `decode_cj_insn()`, `decode_compressed_load_insn()`, `decode_compressed_store_insn()`, `decode_cr_insn()`, `decode_cs_insn()`, `decode_csr_insn()`, `decode_expanded_insn()`, `decode_fence()`, `decode_i_funnelshift_insn()`, `decode_i_insn()`, `decode_i_jalr_insn()`, `decode_i_shift_insn()`, `decode_j_insn()`, `decode_load_insn()`, `decode_mnemonic()`, `decode_r1_insn()`, `decode_r_cmixcmov_insn()`, `decode_r_funnelshift_insn()`, `decode_r_insn()`, `decode_store_insn()`, `decode_u_insn()`, `decode_Zc_cu_insn()`, `decode_Zc_load_insn()`, `decode_Zc_store_insn()`, `decode_Zcmp_cmmv_insn()`, `decode_Zcmp_cmpp_insn()`, `get_csr_name()`, `get_fence_description()`, `printbuffer_dumpline()`, `reg_addr_to_abi_str()`, `reg_addr_to_str()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (15 nodes): `ibex_compressed_decoder.sv`, `ibex_compressed_decoder`, `cm_mv_reg()`, `cm_mva01s()`, `cm_mvsa01()`, `cm_pop_load_reg()`, `cm_push_store_reg()`, `cm_ret_ra()`, `cm_rlist_init()`, `cm_rlist_top_reg()`, `cm_sp_addi()`, `cm_stack_adj()`, `cm_stack_adj_base()`, `cm_stack_adj_word()`, `cm_zero_a0()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (6 nodes): `ibex_pmp.sv`, `ibex_pmp`, `access_fault_check()`, `mml_perm_check()`, `orig_perm_check()`, `perm_check_wrapper()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (3 nodes): `ibex_fetch_fifo`, `ibex_prefetch_buffer.sv`, `ibex_prefetch_buffer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (2 nodes): `ibex_counter.sv`, `ibex_counter`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (2 nodes): `ibex_csr.sv`, `ibex_csr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `ibex_fetch_fifo.sv`, `ibex_fetch_fifo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `ibex_register_file_ff.sv`, `ibex_register_file_ff`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `ibex_register_file_fpga.sv`, `ibex_register_file_fpga`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ibex_pkg` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.341) - this node is a cross-community bridge._
- **Why does `ibex_compressed_decoder` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `ibex_core` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ibex_core` (e.g. with `ibex_ex_block` and `ibex_load_store_unit`) actually correct?**
  _`ibex_core` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ibex_top` (e.g. with `prim_clock_gating` and `prim_buf`) actually correct?**
  _`ibex_top` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ibex_if_stage`, `ibex_id_stage`, `ibex_ex_block` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._