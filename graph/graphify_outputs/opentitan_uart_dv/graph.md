# Graphify Structural Visualization

Manifest: `sources.json`

## Snapshot

- Files: 382
- UVM-related files: 319
- Entities: 484
- Heuristic edges: 489

## Mermaid overview

```mermaid
graph TD
    alert_base_driver["alert_base_driver"]
    dv_base_driver["dv_base_driver"]
    alert_base_driver -->|extends| dv_base_driver
    alert_esc_agent["alert_esc_agent"]
    dv_base_agent["dv_base_agent"]
    alert_esc_agent -->|extends| dv_base_agent
    alert_esc_agent_cfg["alert_esc_agent_cfg"]
    dv_base_agent_cfg["dv_base_agent_cfg"]
    alert_esc_agent_cfg -->|extends| dv_base_agent_cfg
    alert_esc_agent_cov["alert_esc_agent_cov"]
    dv_base_agent_cov["dv_base_agent_cov"]
    alert_esc_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_alert_esc_agent_alert_esc_agent_pkg_sv["hw/dv/sv/alert_esc_agent/alert_esc_agent_pkg.sv"]
    uvm_pkg___["uvm_pkg::*"]
    hw_dv_sv_alert_esc_agent_alert_esc_agent_pkg_sv -->|imports| uvm_pkg___
    dv_lib_pkg___["dv_lib_pkg::*"]
    hw_dv_sv_alert_esc_agent_alert_esc_agent_pkg_sv -->|imports| dv_lib_pkg___
    dv_utils_pkg___["dv_utils_pkg::*"]
    hw_dv_sv_alert_esc_agent_alert_esc_agent_pkg_sv -->|imports| dv_utils_pkg___
    alert_esc_base_monitor["alert_esc_base_monitor"]
    dv_base_monitor["dv_base_monitor"]
    alert_esc_base_monitor -->|extends| dv_base_monitor
    hw_dv_sv_alert_esc_agent_alert_esc_if_sv["hw/dv/sv/alert_esc_agent/alert_esc_if.sv"]
    hw_dv_sv_alert_esc_agent_alert_esc_if_sv -->|imports| uvm_pkg___
    alert_esc_seq_item["alert_esc_seq_item"]
    uvm_sequence_item["uvm_sequence_item"]
    alert_esc_seq_item -->|extends| uvm_sequence_item
    alert_esc_sequencer["alert_esc_sequencer"]
    dv_base_sequencer["dv_base_sequencer"]
    alert_esc_sequencer -->|extends| dv_base_sequencer
    esc_receiver_driver["esc_receiver_driver"]
    esc_receiver_driver -->|extends| dv_base_driver
    esc_sender_driver["esc_sender_driver"]
    esc_sender_driver -->|extends| dv_base_driver
    alert_receiver_base_seq["alert_receiver_base_seq"]
    dv_base_seq["dv_base_seq"]
    alert_receiver_base_seq -->|extends| dv_base_seq
    alert_receiver_ping_seq["alert_receiver_ping_seq"]
    alert_receiver_ping_seq -->|extends| dv_base_seq
    alert_sender_base_seq["alert_sender_base_seq"]
    alert_sender_base_seq -->|extends| dv_base_seq
    esc_receiver_base_seq["esc_receiver_base_seq"]
    esc_receiver_base_seq -->|extends| dv_base_seq
    hw_dv_sv_cip_lib_cip_base_env_cov_sv["hw/dv/sv/cip_lib/cip_base_env_cov.sv"]
    covergroup["covergroup"]
    hw_dv_sv_cip_lib_cip_base_env_cov_sv -->|instantiates| covergroup
    hw_dv_sv_cip_lib_cip_base_pkg_sv["hw/dv/sv/cip_lib/cip_base_pkg.sv"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| uvm_pkg___
    bus_params_pkg___["bus_params_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| bus_params_pkg___
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| dv_utils_pkg___
    csr_utils_pkg___["csr_utils_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| csr_utils_pkg___
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| dv_lib_pkg___
    dv_base_reg_pkg___["dv_base_reg_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| dv_base_reg_pkg___
    tlul_pkg___["tlul_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| tlul_pkg___
    tl_agent_pkg___["tl_agent_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| tl_agent_pkg___
    alert_esc_agent_pkg___["alert_esc_agent_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| alert_esc_agent_pkg___
    push_pull_agent_pkg___["push_pull_agent_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| push_pull_agent_pkg___
    mem_model_pkg___["mem_model_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| mem_model_pkg___
    prim_mubi_pkg___["prim_mubi_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| prim_mubi_pkg___
    sec_cm_pkg___["sec_cm_pkg::*"]
    hw_dv_sv_cip_lib_cip_base_pkg_sv -->|imports| sec_cm_pkg___
    hw_dv_sv_cip_lib_cip_lc_tx_cov_if_sv["hw/dv/sv/cip_lib/cip_lc_tx_cov_if.sv"]
    hw_dv_sv_cip_lib_cip_lc_tx_cov_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_cip_lib_cip_lc_tx_cov_if_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_cip_lib_cip_mubi_cov_if_sv["hw/dv/sv/cip_lib/cip_mubi_cov_if.sv"]
    hw_dv_sv_cip_lib_cip_mubi_cov_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_cip_lib_cip_mubi_cov_if_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_common_ifs_clk_rst_if_sv["hw/dv/sv/common_ifs/clk_rst_if.sv"]
    hw_dv_sv_common_ifs_clk_rst_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_common_ifs_common_ifs_pkg_sv["hw/dv/sv/common_ifs/common_ifs_pkg.sv"]
    hw_dv_sv_common_ifs_common_ifs_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_common_ifs_rst_shadowed_if_sv["hw/dv/sv/common_ifs/rst_shadowed_if.sv"]
    hw_dv_sv_common_ifs_rst_shadowed_if_sv -->|imports| uvm_pkg___
    csr_base_seq["csr_base_seq"]
    uvm_reg_sequence["uvm_reg_sequence"]
    csr_base_seq -->|extends| uvm_reg_sequence
    csr_hw_reset_seq["csr_hw_reset_seq"]
    csr_hw_reset_seq -->|extends| csr_base_seq
    csr_write_seq["csr_write_seq"]
    csr_write_seq -->|extends| csr_base_seq
    csr_rw_seq["csr_rw_seq"]
    csr_rw_seq -->|extends| csr_base_seq
    csr_bit_bash_seq["csr_bit_bash_seq"]
    csr_bit_bash_seq -->|extends| csr_base_seq
    csr_aliasing_seq["csr_aliasing_seq"]
    csr_aliasing_seq -->|extends| csr_base_seq
    csr_mem_walk_seq["csr_mem_walk_seq"]
    csr_mem_walk_seq -->|extends| csr_base_seq
    hw_dv_sv_csr_utils_csr_utils_pkg_sv["hw/dv/sv/csr_utils/csr_utils_pkg.sv"]
    hw_dv_sv_csr_utils_csr_utils_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_csr_utils_csr_utils_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_csr_utils_csr_utils_pkg_sv -->|imports| dv_base_reg_pkg___
    csrng_agent["csrng_agent"]
    csrng_agent -->|extends| dv_base_agent
    csrng_agent_cfg["csrng_agent_cfg"]
    csrng_agent_cfg -->|extends| dv_base_agent_cfg
    csrng_agent_cov["csrng_agent_cov"]
    csrng_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_csrng_agent_csrng_agent_pkg_sv["hw/dv/sv/csrng_agent/csrng_agent_pkg.sv"]
    hw_dv_sv_csrng_agent_csrng_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_csrng_agent_csrng_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_csrng_agent_csrng_agent_pkg_sv -->|imports| dv_lib_pkg___
    csrng_driver["csrng_driver"]
    csrng_driver -->|extends| dv_base_driver
    csrng_item["csrng_item"]
    csrng_item -->|extends| uvm_sequence_item
    csrng_monitor["csrng_monitor"]
    csrng_monitor -->|extends| dv_base_monitor
    csrng_sequencer["csrng_sequencer"]
    csrng_sequencer -->|extends| dv_base_sequencer
    csrng_base_seq["csrng_base_seq"]
    csrng_base_seq -->|extends| dv_base_seq
    csr_excl_item["csr_excl_item"]
    uvm_object["uvm_object"]
    csr_excl_item -->|extends| uvm_object
    dv_base_lockable_field_cov["dv_base_lockable_field_cov"]
    dv_base_lockable_field_cov -->|extends| uvm_object
    hw_dv_sv_dv_base_reg_dv_base_lockable_field_cov_sv["hw/dv/sv/dv_base_reg/dv_base_lockable_field_cov.sv"]
    hw_dv_sv_dv_base_reg_dv_base_lockable_field_cov_sv -->|instantiates| covergroup
    mubi32_cov["mubi32_cov"]
    mubi32_cov -->|extends| uvm_object
    dv_base_mubi_cov["dv_base_mubi_cov"]
    dv_base_mubi_cov -->|extends| uvm_object
    hw_dv_sv_dv_base_reg_dv_base_mubi_cov_sv["hw/dv/sv/dv_base_reg/dv_base_mubi_cov.sv"]
    hw_dv_sv_dv_base_reg_dv_base_mubi_cov_sv -->|instantiates| covergroup
    dv_base_reg["dv_base_reg"]
    uvm_reg["uvm_reg"]
    dv_base_reg -->|extends| uvm_reg
    dv_base_reg_block["dv_base_reg_block"]
    uvm_reg_block["uvm_reg_block"]
    dv_base_reg_block -->|extends| uvm_reg_block
    hw_dv_sv_dv_base_reg_dv_base_reg_pkg_sv["hw/dv/sv/dv_base_reg/dv_base_reg_pkg.sv"]
    hw_dv_sv_dv_base_reg_dv_base_reg_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_dv_base_reg_dv_base_reg_pkg_sv -->|imports| dv_utils_pkg___
    dv_base_shadowed_field_cov["dv_base_shadowed_field_cov"]
    dv_base_shadowed_field_cov -->|extends| uvm_object
    hw_dv_sv_dv_base_reg_dv_base_shadowed_field_cov_sv["hw/dv/sv/dv_base_reg/dv_base_shadowed_field_cov.sv"]
    hw_dv_sv_dv_base_reg_dv_base_shadowed_field_cov_sv -->|instantiates| covergroup
    hw_dv_sv_dv_lib_bit_toggle_cg_wrap_sv["hw/dv/sv/dv_lib/bit_toggle_cg_wrap.sv"]
    hw_dv_sv_dv_lib_bit_toggle_cg_wrap_sv -->|instantiates| covergroup
    dv_base_agent_cfg -->|extends| uvm_object
    hw_dv_sv_dv_lib_dv_lib_pkg_sv["hw/dv/sv/dv_lib/dv_lib_pkg.sv"]
    hw_dv_sv_dv_lib_dv_lib_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_dv_lib_dv_lib_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_dv_lib_dv_lib_pkg_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_dv_utils_dv_utils_pkg_sv["hw/dv/sv/dv_utils/dv_utils_pkg.sv"]
    hw_dv_sv_dv_utils_dv_utils_pkg_sv -->|imports| uvm_pkg___
    entropy_src_xht_agent["entropy_src_xht_agent"]
    entropy_src_xht_agent -->|extends| dv_base_agent
    entropy_src_xht_agent_cfg["entropy_src_xht_agent_cfg"]
    entropy_src_xht_agent_cfg -->|extends| dv_base_agent_cfg
    hw_dv_sv_entropy_src_xht_agent_entropy_src_xht_agent_pkg_sv["hw/dv/sv/entropy_src_xht_agent/entropy_src_xht_agent_pkg.sv"]
    hw_dv_sv_entropy_src_xht_agent_entropy_src_xht_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_entropy_src_xht_agent_entropy_src_xht_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_entropy_src_xht_agent_entropy_src_xht_agent_pkg_sv -->|imports| dv_lib_pkg___
    entropy_src_xht_device_driver["entropy_src_xht_device_driver"]
    entropy_src_xht_device_driver -->|extends| dv_base_driver
    entropy_src_xht_item["entropy_src_xht_item"]
    entropy_src_xht_item -->|extends| uvm_sequence_item
    entropy_src_xht_monitor["entropy_src_xht_monitor"]
    entropy_src_xht_monitor -->|extends| dv_base_monitor
    entropy_src_xht_sequencer["entropy_src_xht_sequencer"]
    entropy_src_xht_sequencer -->|extends| dv_base_sequencer
    entropy_src_xht_base_device_seq["entropy_src_xht_base_device_seq"]
    entropy_src_xht_base_device_seq -->|extends| dv_base_seq
    flash_phy_prim_agent["flash_phy_prim_agent"]
    flash_phy_prim_agent -->|extends| dv_base_agent
    flash_phy_prim_agent_cfg["flash_phy_prim_agent_cfg"]
    flash_phy_prim_agent_cfg -->|extends| dv_base_agent_cfg
    flash_phy_prim_agent_cov["flash_phy_prim_agent_cov"]
    flash_phy_prim_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_flash_phy_prim_agent_flash_phy_prim_agent_pkg_sv["hw/dv/sv/flash_phy_prim_agent/flash_phy_prim_agent_pkg.sv"]
    hw_dv_sv_flash_phy_prim_agent_flash_phy_prim_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_flash_phy_prim_agent_flash_phy_prim_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_flash_phy_prim_agent_flash_phy_prim_agent_pkg_sv -->|imports| dv_lib_pkg___
    flash_phy_prim_driver["flash_phy_prim_driver"]
    flash_phy_prim_driver -->|extends| dv_base_driver
    flash_phy_prim_item["flash_phy_prim_item"]
    flash_phy_prim_item -->|extends| uvm_sequence_item
    flash_phy_prim_monitor["flash_phy_prim_monitor"]
    flash_phy_prim_monitor -->|extends| dv_base_monitor
    flash_phy_prim_base_seq["flash_phy_prim_base_seq"]
    flash_phy_prim_base_seq -->|extends| dv_base_seq
    i2c_acqdata_item["i2c_acqdata_item"]
    i2c_acqdata_item -->|extends| uvm_sequence_item
    i2c_agent["i2c_agent"]
    i2c_agent -->|extends| dv_base_agent
    i2c_agent_cfg["i2c_agent_cfg"]
    i2c_agent_cfg -->|extends| dv_base_agent_cfg
    i2c_agent_cov["i2c_agent_cov"]
    i2c_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_i2c_agent_i2c_agent_pkg_sv["hw/dv/sv/i2c_agent/i2c_agent_pkg.sv"]
    hw_dv_sv_i2c_agent_i2c_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_i2c_agent_i2c_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_i2c_agent_i2c_agent_pkg_sv -->|imports| dv_lib_pkg___
    i2c_driver["i2c_driver"]
    i2c_driver -->|extends| dv_base_driver
    i2c_fdata_item["i2c_fdata_item"]
    i2c_fdata_item -->|extends| uvm_sequence_item
    hw_dv_sv_i2c_agent_i2c_if_sv["hw/dv/sv/i2c_agent/i2c_if.sv"]
    hw_dv_sv_i2c_agent_i2c_if_sv -->|imports| uvm_pkg___
    i2c_item["i2c_item"]
    i2c_item -->|extends| uvm_sequence_item
    i2c_monitor["i2c_monitor"]
    i2c_monitor -->|extends| dv_base_monitor
    i2c_sequencer["i2c_sequencer"]
    i2c_sequencer -->|extends| dv_base_sequencer
    i2c_base_seq["i2c_base_seq"]
    i2c_base_seq -->|extends| dv_base_seq
    jtag_agent["jtag_agent"]
    jtag_agent -->|extends| dv_base_agent
    jtag_agent_cfg["jtag_agent_cfg"]
    jtag_agent_cfg -->|extends| dv_base_agent_cfg
    jtag_agent_cov["jtag_agent_cov"]
    jtag_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_jtag_agent_jtag_agent_pkg_sv["hw/dv/sv/jtag_agent/jtag_agent_pkg.sv"]
    hw_dv_sv_jtag_agent_jtag_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_jtag_agent_jtag_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_jtag_agent_jtag_agent_pkg_sv -->|imports| dv_lib_pkg___
    hw_dv_sv_jtag_agent_jtag_agent_pkg_sv -->|imports| dv_base_reg_pkg___
    jtag_driver["jtag_driver"]
    jtag_driver -->|extends| dv_base_driver
    jtag_dtm_base_reg["jtag_dtm_base_reg"]
    jtag_dtm_base_reg -->|extends| dv_base_reg
    jtag_dtm_reg_block["jtag_dtm_reg_block"]
    jtag_dtm_reg_block -->|extends| dv_base_reg_block
    jtag_item["jtag_item"]
    jtag_item -->|extends| uvm_sequence_item
    jtag_monitor["jtag_monitor"]
    jtag_monitor -->|extends| dv_base_monitor
    jtag_base_seq["jtag_base_seq"]
    jtag_base_seq -->|extends| dv_base_seq
    hw_dv_sv_jtag_dmi_agent_jtag_dmi_agent_pkg_sv["hw/dv/sv/jtag_dmi_agent/jtag_dmi_agent_pkg.sv"]
    hw_dv_sv_jtag_dmi_agent_jtag_dmi_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_dmi_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_dmi_agent_pkg_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_dmi_agent_pkg_sv -->|imports| dv_lib_pkg___
    jtag_dmi_item["jtag_dmi_item"]
    jtag_dmi_item -->|extends| uvm_sequence_item
    jtag_dmi_reg_abstractdata["jtag_dmi_reg_abstractdata"]
    jtag_dmi_reg_abstractdata -->|extends| dv_base_reg
    jtag_dmi_reg_dmcontrol["jtag_dmi_reg_dmcontrol"]
    jtag_dmi_reg_dmcontrol -->|extends| dv_base_reg
    jtag_dmi_reg_dmstatus["jtag_dmi_reg_dmstatus"]
    jtag_dmi_reg_dmstatus -->|extends| dv_base_reg
    jtag_dmi_reg_hartinfo["jtag_dmi_reg_hartinfo"]
    jtag_dmi_reg_hartinfo -->|extends| dv_base_reg
    jtag_dmi_reg_haltsum1["jtag_dmi_reg_haltsum1"]
    jtag_dmi_reg_haltsum1 -->|extends| dv_base_reg
    jtag_dmi_reg_abstractcs["jtag_dmi_reg_abstractcs"]
    jtag_dmi_reg_abstractcs -->|extends| dv_base_reg
    jtag_dmi_reg_command["jtag_dmi_reg_command"]
    jtag_dmi_reg_command -->|extends| dv_base_reg
    jtag_dmi_reg_abstractauto["jtag_dmi_reg_abstractauto"]
    jtag_dmi_reg_abstractauto -->|extends| dv_base_reg
    jtag_dmi_reg_progbuf["jtag_dmi_reg_progbuf"]
    jtag_dmi_reg_progbuf -->|extends| dv_base_reg
    jtag_dmi_reg_haltsum2["jtag_dmi_reg_haltsum2"]
    jtag_dmi_reg_haltsum2 -->|extends| dv_base_reg
    jtag_dmi_reg_haltsum3["jtag_dmi_reg_haltsum3"]
    jtag_dmi_reg_haltsum3 -->|extends| dv_base_reg
    jtag_dmi_reg_sbcs["jtag_dmi_reg_sbcs"]
    jtag_dmi_reg_sbcs -->|extends| dv_base_reg
    jtag_dmi_reg_sbaddress0["jtag_dmi_reg_sbaddress0"]
    jtag_dmi_reg_sbaddress0 -->|extends| dv_base_reg
    jtag_dmi_reg_sbaddress1["jtag_dmi_reg_sbaddress1"]
    jtag_dmi_reg_sbaddress1 -->|extends| dv_base_reg
    jtag_dmi_reg_sbaddress2["jtag_dmi_reg_sbaddress2"]
    jtag_dmi_reg_sbaddress2 -->|extends| dv_base_reg
    jtag_dmi_reg_sbaddress3["jtag_dmi_reg_sbaddress3"]
    jtag_dmi_reg_sbaddress3 -->|extends| dv_base_reg
    jtag_dmi_reg_sbdata0["jtag_dmi_reg_sbdata0"]
    jtag_dmi_reg_sbdata0 -->|extends| dv_base_reg
    jtag_dmi_reg_sbdata1["jtag_dmi_reg_sbdata1"]
    jtag_dmi_reg_sbdata1 -->|extends| dv_base_reg
    jtag_dmi_reg_sbdata2["jtag_dmi_reg_sbdata2"]
    jtag_dmi_reg_sbdata2 -->|extends| dv_base_reg
    jtag_dmi_reg_sbdata3["jtag_dmi_reg_sbdata3"]
    jtag_dmi_reg_sbdata3 -->|extends| dv_base_reg
    jtag_dmi_reg_haltsum0["jtag_dmi_reg_haltsum0"]
    jtag_dmi_reg_haltsum0 -->|extends| dv_base_reg
    jtag_dmi_reg_block["jtag_dmi_reg_block"]
    jtag_dmi_reg_block -->|extends| dv_base_reg_block
    jtag_rv_debugger["jtag_rv_debugger"]
    jtag_rv_debugger -->|extends| uvm_object
    hw_dv_sv_jtag_dmi_agent_jtag_rv_debugger_pkg_sv["hw/dv/sv/jtag_dmi_agent/jtag_rv_debugger_pkg.sv"]
    hw_dv_sv_jtag_dmi_agent_jtag_rv_debugger_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_rv_debugger_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_rv_debugger_pkg_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_jtag_dmi_agent_jtag_rv_debugger_pkg_sv -->|imports| dv_lib_pkg___
    sba_access_item["sba_access_item"]
    sba_access_item -->|extends| uvm_sequence_item
    jtag_riscv_agent["jtag_riscv_agent"]
    jtag_riscv_agent -->|extends| dv_base_agent
    jtag_riscv_agent_cfg["jtag_riscv_agent_cfg"]
    jtag_riscv_agent_cfg -->|extends| dv_base_agent_cfg
    jtag_riscv_agent_cov["jtag_riscv_agent_cov"]
    jtag_riscv_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_jtag_riscv_agent_jtag_riscv_agent_pkg_sv["hw/dv/sv/jtag_riscv_agent/jtag_riscv_agent_pkg.sv"]
    hw_dv_sv_jtag_riscv_agent_jtag_riscv_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_jtag_riscv_agent_jtag_riscv_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_jtag_riscv_agent_jtag_riscv_agent_pkg_sv -->|imports| dv_lib_pkg___
    jtag_riscv_driver["jtag_riscv_driver"]
    jtag_riscv_driver -->|extends| dv_base_driver
    jtag_riscv_item["jtag_riscv_item"]
    jtag_riscv_item -->|extends| uvm_sequence_item
    jtag_riscv_monitor["jtag_riscv_monitor"]
    jtag_riscv_monitor -->|extends| dv_base_monitor
    jtag_riscv_sequencer["jtag_riscv_sequencer"]
    jtag_riscv_sequencer -->|extends| dv_base_sequencer
    jtag_riscv_base_seq["jtag_riscv_base_seq"]
    jtag_riscv_base_seq -->|extends| dv_base_seq
    hw_dv_sv_key_sideload_agent_key_sideload_agent_pkg_sv["hw/dv/sv/key_sideload_agent/key_sideload_agent_pkg.sv"]
    hw_dv_sv_key_sideload_agent_key_sideload_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_key_sideload_agent_key_sideload_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_key_sideload_agent_key_sideload_agent_pkg_sv -->|imports| dv_lib_pkg___
    kmac_app_agent["kmac_app_agent"]
    kmac_app_agent -->|extends| dv_base_agent
    kmac_app_agent_cfg["kmac_app_agent_cfg"]
    kmac_app_agent_cfg -->|extends| dv_base_agent_cfg
    kmac_app_agent_cov["kmac_app_agent_cov"]
    kmac_app_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_kmac_app_agent_kmac_app_agent_pkg_sv["hw/dv/sv/kmac_app_agent/kmac_app_agent_pkg.sv"]
    hw_dv_sv_kmac_app_agent_kmac_app_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_kmac_app_agent_kmac_app_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_kmac_app_agent_kmac_app_agent_pkg_sv -->|imports| dv_lib_pkg___
    kmac_app_driver["kmac_app_driver"]
    kmac_app_driver -->|extends| dv_base_driver
    kmac_app_item["kmac_app_item"]
    kmac_app_item -->|extends| uvm_sequence_item
    kmac_app_monitor["kmac_app_monitor"]
    kmac_app_monitor -->|extends| dv_base_monitor
    kmac_app_sequencer["kmac_app_sequencer"]
    kmac_app_sequencer -->|extends| dv_base_sequencer
    kmac_app_base_seq["kmac_app_base_seq"]
    kmac_app_base_seq -->|extends| dv_base_seq
    hw_dv_sv_mem_bkdr_scb_mem_bkdr_scb_sv["hw/dv/sv/mem_bkdr_scb/mem_bkdr_scb.sv"]
    hw_dv_sv_mem_bkdr_scb_mem_bkdr_scb_sv -->|instantiates| covergroup
    hw_dv_sv_mem_bkdr_scb_mem_bkdr_scb_pkg_sv["hw/dv/sv/mem_bkdr_scb/mem_bkdr_scb_pkg.sv"]
    hw_dv_sv_mem_bkdr_scb_mem_bkdr_scb_pkg_sv -->|imports| uvm_pkg___
    mem_bkdr_util["mem_bkdr_util"]
    mem_bkdr_util -->|extends| uvm_object
    hw_dv_sv_mem_bkdr_util_mem_bkdr_util_pkg_sv["hw/dv/sv/mem_bkdr_util/mem_bkdr_util_pkg.sv"]
    hw_dv_sv_mem_bkdr_util_mem_bkdr_util_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_mem_model_mem_model_pkg_sv["hw/dv/sv/mem_model/mem_model_pkg.sv"]
    hw_dv_sv_mem_model_mem_model_pkg_sv -->|imports| uvm_pkg___
    pattgen_agent["pattgen_agent"]
    pattgen_agent -->|extends| dv_base_agent
    pattgen_agent_cfg["pattgen_agent_cfg"]
    pattgen_agent_cfg -->|extends| dv_base_agent_cfg
    pattgen_agent_cov["pattgen_agent_cov"]
    pattgen_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_pattgen_agent_pattgen_agent_pkg_sv["hw/dv/sv/pattgen_agent/pattgen_agent_pkg.sv"]
    hw_dv_sv_pattgen_agent_pattgen_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_pattgen_agent_pattgen_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_pattgen_agent_pattgen_agent_pkg_sv -->|imports| dv_lib_pkg___
    pattgen_driver["pattgen_driver"]
    pattgen_driver -->|extends| dv_base_driver
    pattgen_item["pattgen_item"]
    pattgen_item -->|extends| uvm_sequence_item
    pattgen_monitor["pattgen_monitor"]
    pattgen_monitor -->|extends| dv_base_monitor
    hw_dv_sv_push_pull_agent_push_pull_agent_cov_sv["hw/dv/sv/push_pull_agent/push_pull_agent_cov.sv"]
    hw_dv_sv_push_pull_agent_push_pull_agent_cov_sv -->|instantiates| covergroup
    hw_dv_sv_push_pull_agent_push_pull_agent_pkg_sv["hw/dv/sv/push_pull_agent/push_pull_agent_pkg.sv"]
    hw_dv_sv_push_pull_agent_push_pull_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_push_pull_agent_push_pull_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_push_pull_agent_push_pull_agent_pkg_sv -->|imports| dv_lib_pkg___
    pwm_item["pwm_item"]
    pwm_item -->|extends| uvm_sequence_item
    pwm_monitor["pwm_monitor"]
    pwm_monitor -->|extends| dv_base_monitor
    pwm_monitor_cfg["pwm_monitor_cfg"]
    pwm_monitor_cfg -->|extends| dv_base_agent_cfg
    hw_dv_sv_pwm_monitor_pwm_monitor_pkg_sv["hw/dv/sv/pwm_monitor/pwm_monitor_pkg.sv"]
    hw_dv_sv_pwm_monitor_pwm_monitor_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_pwm_monitor_pwm_monitor_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_pwm_monitor_pwm_monitor_pkg_sv -->|imports| dv_lib_pkg___
    rng_agent["rng_agent"]
    rng_agent -->|extends| dv_base_agent
    rng_agent_cfg["rng_agent_cfg"]
    rng_agent_cfg -->|extends| dv_base_agent_cfg
    rng_agent_cov["rng_agent_cov"]
    rng_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_rng_agent_rng_agent_pkg_sv["hw/dv/sv/rng_agent/rng_agent_pkg.sv"]
    hw_dv_sv_rng_agent_rng_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_rng_agent_rng_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_rng_agent_rng_agent_pkg_sv -->|imports| dv_lib_pkg___
    rng_driver["rng_driver"]
    rng_driver -->|extends| dv_base_driver
    rng_item["rng_item"]
    rng_item -->|extends| uvm_sequence_item
    rng_monitor["rng_monitor"]
    rng_monitor -->|extends| dv_base_monitor
    rng_base_seq["rng_base_seq"]
    rng_base_seq -->|extends| dv_base_seq
    hw_dv_sv_scoreboard_scoreboard_pkg_sv["hw/dv/sv/scoreboard/scoreboard_pkg.sv"]
    hw_dv_sv_scoreboard_scoreboard_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_scoreboard_scoreboard_pkg_sv -->|imports| dv_lib_pkg___
    hw_dv_sv_scoreboard_scoreboard_pkg_sv -->|imports| dv_base_reg_pkg___
    hw_dv_sv_sec_cm_prim_count_if_sv["hw/dv/sv/sec_cm/prim_count_if.sv"]
    hw_dv_sv_sec_cm_prim_count_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_sec_cm_prim_double_lfsr_if_sv["hw/dv/sv/sec_cm/prim_double_lfsr_if.sv"]
    hw_dv_sv_sec_cm_prim_double_lfsr_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_sec_cm_prim_onehot_check_if_sv["hw/dv/sv/sec_cm/prim_onehot_check_if.sv"]
    hw_dv_sv_sec_cm_prim_onehot_check_if_sv -->|instantiates| covergroup
    hw_dv_sv_sec_cm_prim_onehot_check_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_sec_cm_prim_singleton_fifo_if_sv["hw/dv/sv/sec_cm/prim_singleton_fifo_if.sv"]
    hw_dv_sv_sec_cm_prim_singleton_fifo_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_sec_cm_prim_sparse_fsm_flop_if_sv["hw/dv/sv/sec_cm/prim_sparse_fsm_flop_if.sv"]
    hw_dv_sv_sec_cm_prim_sparse_fsm_flop_if_sv -->|imports| uvm_pkg___
    sec_cm_base_if_proxy["sec_cm_base_if_proxy"]
    sec_cm_base_if_proxy -->|extends| uvm_object
    hw_dv_sv_sec_cm_sec_cm_pkg_sv["hw/dv/sv/sec_cm/sec_cm_pkg.sv"]
    hw_dv_sv_sec_cm_sec_cm_pkg_sv -->|imports| uvm_pkg___
    spi_base_seq["spi_base_seq"]
    spi_base_seq -->|extends| dv_base_seq
    spi_device_dma_seq["spi_device_dma_seq"]
    spi_device_dma_seq -->|extends| spi_base_seq
    spi_device_flash_seq["spi_device_flash_seq"]
    spi_device_flash_seq -->|extends| dv_base_seq
    spi_device_seq["spi_device_seq"]
    spi_device_seq -->|extends| spi_base_seq
    spi_host_dummy_seq["spi_host_dummy_seq"]
    spi_host_dummy_seq -->|extends| spi_base_seq
    spi_host_flash_seq["spi_host_flash_seq"]
    spi_host_flash_seq -->|extends| spi_base_seq
    spi_host_seq["spi_host_seq"]
    spi_host_seq -->|extends| spi_base_seq
    spi_host_tpm_seq["spi_host_tpm_seq"]
    spi_host_tpm_seq -->|extends| spi_base_seq
    spi_agent["spi_agent"]
    spi_agent -->|extends| dv_base_agent
    spi_agent_cfg["spi_agent_cfg"]
    spi_agent_cfg -->|extends| dv_base_agent_cfg
    spi_agent_cov["spi_agent_cov"]
    spi_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_spi_agent_spi_agent_pkg_sv["hw/dv/sv/spi_agent/spi_agent_pkg.sv"]
    hw_dv_sv_spi_agent_spi_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_spi_agent_spi_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_spi_agent_spi_agent_pkg_sv -->|imports| dv_lib_pkg___
    spi_driver["spi_driver"]
    spi_driver -->|extends| dv_base_driver
    spi_flash_cmd_info["spi_flash_cmd_info"]
    spi_flash_cmd_info -->|extends| uvm_sequence_item
    hw_dv_sv_spi_agent_spi_if_sv["hw/dv/sv/spi_agent/spi_if.sv"]
    hw_dv_sv_spi_agent_spi_if_sv -->|imports| uvm_pkg___
    spi_item["spi_item"]
    spi_item -->|extends| uvm_sequence_item
    spi_monitor["spi_monitor"]
    spi_monitor -->|extends| dv_base_monitor
    spi_sequencer["spi_sequencer"]
    spi_sequencer -->|extends| dv_base_sequencer
    hw_dv_sv_sw_logger_if_sw_logger_if_sv["hw/dv/sv/sw_logger_if/sw_logger_if.sv"]
    hw_dv_sv_sw_logger_if_sw_logger_if_sv -->|imports| uvm_pkg___
    hw_dv_sv_test_vectors_test_vectors_pkg_sv["hw/dv/sv/test_vectors/test_vectors_pkg.sv"]
    hw_dv_sv_test_vectors_test_vectors_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_tl_agent_dv_env_tl_agent_env_pkg_sv["hw/dv/sv/tl_agent/dv/env/tl_agent_env_pkg.sv"]
    hw_dv_sv_tl_agent_dv_env_tl_agent_env_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_tl_agent_dv_env_tl_agent_env_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_tl_agent_dv_env_tl_agent_env_pkg_sv -->|imports| dv_lib_pkg___
    hw_dv_sv_tl_agent_dv_tb_tb_sv["hw/dv/sv/tl_agent/dv/tb/tb.sv"]
    hw_dv_sv_tl_agent_dv_tb_tb_sv -->|imports| uvm_pkg___
    hw_dv_sv_tl_agent_dv_tb_tb_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_tl_agent_dv_tests_tl_agent_test_pkg_sv["hw/dv/sv/tl_agent/dv/tests/tl_agent_test_pkg.sv"]
    hw_dv_sv_tl_agent_dv_tests_tl_agent_test_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_tl_agent_dv_tests_tl_agent_test_pkg_sv -->|imports| dv_lib_pkg___
    tl_agent["tl_agent"]
    tl_agent -->|extends| dv_base_agent
    tl_agent_cfg["tl_agent_cfg"]
    tl_agent_cfg -->|extends| dv_base_agent_cfg
    tl_agent_cov["tl_agent_cov"]
    tl_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_tl_agent_tl_agent_cov_sv["hw/dv/sv/tl_agent/tl_agent_cov.sv"]
    hw_dv_sv_tl_agent_tl_agent_cov_sv -->|instantiates| covergroup
    hw_dv_sv_tl_agent_tl_agent_pkg_sv["hw/dv/sv/tl_agent/tl_agent_pkg.sv"]
    hw_dv_sv_tl_agent_tl_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_tl_agent_tl_agent_pkg_sv -->|imports| dv_lib_pkg___
    hw_dv_sv_tl_agent_tl_agent_pkg_sv -->|imports| dv_base_reg_pkg___
    tl_monitor["tl_monitor"]
    tl_monitor -->|extends| dv_base_monitor
    tl_seq_item["tl_seq_item"]
    tl_seq_item -->|extends| uvm_sequence_item
    tl_sequencer["tl_sequencer"]
    tl_sequencer -->|extends| dv_base_sequencer
    uart_base_seq["uart_base_seq"]
    uart_base_seq -->|extends| dv_base_seq
    uart_agent["uart_agent"]
    uart_agent -->|extends| dv_base_agent
    uart_agent_cfg["uart_agent_cfg"]
    uart_agent_cfg -->|extends| dv_base_agent_cfg
    uart_agent_cov["uart_agent_cov"]
    uart_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_uart_agent_uart_agent_pkg_sv["hw/dv/sv/uart_agent/uart_agent_pkg.sv"]
    hw_dv_sv_uart_agent_uart_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_uart_agent_uart_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_uart_agent_uart_agent_pkg_sv -->|imports| dv_lib_pkg___
    uart_driver["uart_driver"]
    uart_driver -->|extends| dv_base_driver
    uart_item["uart_item"]
    uart_item -->|extends| uvm_sequence_item
    uart_monitor["uart_monitor"]
    uart_monitor -->|extends| dv_base_monitor
    uart_sequencer["uart_sequencer"]
    uart_sequencer -->|extends| dv_base_sequencer
    usb20_base_seq["usb20_base_seq"]
    usb20_base_seq -->|extends| dv_base_seq
    usb20_agent["usb20_agent"]
    usb20_agent -->|extends| dv_base_agent
    usb20_agent_cfg["usb20_agent_cfg"]
    usb20_agent_cfg -->|extends| dv_base_agent_cfg
    usb20_agent_cov["usb20_agent_cov"]
    usb20_agent_cov -->|extends| dv_base_agent_cov
    hw_dv_sv_usb20_agent_usb20_agent_pkg_sv["hw/dv/sv/usb20_agent/usb20_agent_pkg.sv"]
    hw_dv_sv_usb20_agent_usb20_agent_pkg_sv -->|imports| uvm_pkg___
    hw_dv_sv_usb20_agent_usb20_agent_pkg_sv -->|imports| dv_utils_pkg___
    hw_dv_sv_usb20_agent_usb20_agent_pkg_sv -->|imports| dv_lib_pkg___
    usb20_driver["usb20_driver"]
    usb20_driver -->|extends| dv_base_driver
    usb20_item["usb20_item"]
    usb20_item -->|extends| uvm_sequence_item
    token_pkt["token_pkt"]
    token_pkt -->|extends| usb20_item
    data_pkt["data_pkt"]
    data_pkt -->|extends| usb20_item
    sof_pkt["sof_pkt"]
    sof_pkt -->|extends| usb20_item
    handshake_pkt["handshake_pkt"]
    handshake_pkt -->|extends| usb20_item
    usb20_monitor["usb20_monitor"]
    usb20_monitor -->|extends| dv_base_monitor
    uart_fifo_full_vseq["uart_fifo_full_vseq"]
    uart_tx_rx_vseq["uart_tx_rx_vseq"]
    uart_fifo_full_vseq -->|extends| uart_tx_rx_vseq
    uart_loopback_vseq["uart_loopback_vseq"]
    uart_loopback_vseq -->|extends| uart_tx_rx_vseq
    uart_noise_filter_vseq["uart_noise_filter_vseq"]
    uart_noise_filter_vseq -->|extends| uart_tx_rx_vseq
    uart_rx_oversample_vseq["uart_rx_oversample_vseq"]
    uart_rx_oversample_vseq -->|extends| uart_tx_rx_vseq
    uart_smoke_vseq["uart_smoke_vseq"]
    uart_smoke_vseq -->|extends| uart_tx_rx_vseq
    uart_base_vseq["uart_base_vseq"]
    uart_tx_rx_vseq -->|extends| uart_base_vseq
    hw_ip_uart_dv_env_uart_env_pkg_sv["hw/ip/uart/dv/env/uart_env_pkg.sv"]
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| uvm_pkg___
    top_pkg___["top_pkg::*"]
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| top_pkg___
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| dv_utils_pkg___
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| csr_utils_pkg___
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| tl_agent_pkg___
    uart_agent_pkg___["uart_agent_pkg::*"]
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| uart_agent_pkg___
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| dv_lib_pkg___
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| dv_base_reg_pkg___
    cip_base_pkg___["cip_base_pkg::*"]
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| cip_base_pkg___
    uart_ral_pkg___["uart_ral_pkg::*"]
    hw_ip_uart_dv_env_uart_env_pkg_sv -->|imports| uart_ral_pkg___
    hw_ip_uart_dv_tb_tb_sv["hw/ip/uart/dv/tb/tb.sv"]
    clk_rst_if["clk_rst_if"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| clk_rst_if
    pins_if["pins_if"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| pins_if
    tl_if["tl_if"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| tl_if
    uart_if["uart_if"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| uart_if
    uart_nf_if["uart_nf_if"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| uart_nf_if
    uart["uart"]
    hw_ip_uart_dv_tb_tb_sv -->|instantiates| uart
    hw_ip_uart_dv_tb_tb_sv -->|imports| uvm_pkg___
    hw_ip_uart_dv_tb_tb_sv -->|imports| dv_utils_pkg___
    hw_ip_uart_dv_tb_tb_sv -->|imports| tl_agent_pkg___
    uart_env_pkg___["uart_env_pkg::*"]
    hw_ip_uart_dv_tb_tb_sv -->|imports| uart_env_pkg___
    uart_test_pkg___["uart_test_pkg::*"]
    hw_ip_uart_dv_tb_tb_sv -->|imports| uart_test_pkg___
    hw_ip_uart_dv_tests_uart_test_pkg_sv["hw/ip/uart/dv/tests/uart_test_pkg.sv"]
    hw_ip_uart_dv_tests_uart_test_pkg_sv -->|imports| uvm_pkg___
```

## Largest files

| File | Lines | UVM | run_test | config_db | analysis_port |
| --- | ---: | :---: | :---: | :---: | :---: |
| `hw/ip/uart/rtl/uart_reg_top.sv` | 1916 | N | N | N | N |
| `hw/dv/sv/jtag_dmi_agent/jtag_dmi_reg_block.sv` | 1817 | Y | N | N | N |
| `hw/dv/sv/cip_lib/seq_lib/cip_base_vseq.sv` | 1468 | Y | N | Y | N |
| `hw/dv/sv/jtag_dmi_agent/jtag_rv_debugger.sv` | 1268 | Y | N | N | N |
| `hw/dv/sv/csr_utils/csr_utils_pkg.sv` | 860 | Y | N | N | N |
| `hw/dv/sv/cip_lib/cip_base_scoreboard.sv` | 801 | Y | N | N | N |
| `hw/dv/sv/mem_bkdr_util/mem_bkdr_util.sv` | 746 | Y | N | N | N |
| `hw/dv/sv/usb20_agent/usb20_monitor.sv` | 692 | Y | N | Y | N |
| `hw/dv/sv/dv_utils/dv_macros.svh` | 675 | Y | N | Y | N |
| `hw/dv/sv/i2c_agent/i2c_monitor.sv` | 668 | Y | N | N | Y |

## Notes

- This view is derived from deterministic source scanning, so it remains available even without a Graphify install.
- Use it as a reviewable baseline, then compare against richer Graphify graph exports when available.
