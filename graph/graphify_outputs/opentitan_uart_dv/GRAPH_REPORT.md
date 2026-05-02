# Graph Report - /home/kyungpyo/ws/varuna/project/open-rtl-verification/.cache/graphify_repos/opentitan-master/hw/dv/sv  (2026-05-02)

## Corpus Check
- Large corpus: 371 files · ~365,142 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 367 nodes · 159 edges · 11 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
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

## God Nodes (most connected - your core abstractions)
1. `uvm_pkg` - 46 edges
2. `dv_utils_pkg` - 25 edges
3. `dv_lib_pkg` - 22 edges
4. `dv_base_reg_pkg` - 10 edges
5. `bus_params_pkg` - 6 edges
6. `csr_utils_pkg` - 5 edges
7. `push_pull_agent_pkg` - 3 edges
8. `prim_mubi_pkg` - 3 edges
9. `jtag_agent_pkg` - 3 edges
10. `tlul_pkg` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (5): common_ifs_pkg, i2c_agent_pkg, spi_agent_pkg, str_utils_pkg, uvm_pkg

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (5): dv_lib_pkg, dv_utils_pkg, entropy_src_pkg, flash_ctrl_top_specific_pkg, i2c_pkg

### Community 2 - "Community 2"
Cohesion: 0.21
Nodes (4): csr_utils_pkg, dv_base_reg_pkg, jtag_agent_pkg, jtag_dmi_agent_pkg

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (5): alert_esc_agent_pkg, bus_params_pkg, mem_model_pkg, sec_cm_pkg, tlul_pkg

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (4): csrng_pkg, keymgr_pkg, prim_mubi_pkg, push_pull_agent_pkg

### Community 5 - "Community 5"
Cohesion: 0.4
Nodes (3): tl_agent_env_pkg, tl_agent_pkg, tl_agent_test_pkg

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (2): lc_ctrl_state_pkg, prim_secded_pkg

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (2): prim_alert_pkg, prim_esc_pkg

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): flash_phy_pkg

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): sw_test_status_pkg

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): entropy_subsys_fifo_exception_pkg

## Knowledge Gaps
- **14 isolated node(s):** `common_ifs_pkg`, `entropy_subsys_fifo_exception_pkg`, `sw_test_status_pkg`, `i2c_pkg`, `i2c_agent_pkg` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (5 nodes): `cip_tl_seq_item.sv`, `lc_ctrl_state_pkg`, `mem_bkdr_util_pkg.sv`, `mem_bkdr_util.sv`, `prim_secded_pkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (4 nodes): `alert_esc_agent_pkg.sv`, `prim_alert_pkg`, `prim_esc_pkg`, `sec_cm_pkg.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `flash_phy_pkg`, `flash_phy_prim_if.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (2 nodes): `sw_test_status_pkg`, `sw_test_status_if.sv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `entropy_subsys_fifo_exception_if.sv`, `entropy_subsys_fifo_exception_pkg`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `uvm_pkg` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `dv_utils_pkg` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `dv_lib_pkg` connect `Community 1` to `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `common_ifs_pkg`, `entropy_subsys_fifo_exception_pkg`, `sw_test_status_pkg` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._