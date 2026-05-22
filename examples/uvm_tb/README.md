# Counter UVM Example

Minimal UVM environment for the `examples/rtl/counter.sv` DUT.

## Purpose

This example exists to make early graph-based analysis and UVM-structure extraction concrete.

It intentionally stays small while still exposing the verification relationships that matter:

- virtual interface handoff from top to test
- sequence item and sequencer flow
- driver to DUT pin control
- monitor to analysis port publication
- scoreboard-style checking hook via subscriber
- agent / env / test hierarchy
- package-scoped UVM class collection in a single file for deterministic filelist-driven analysis

## Files

- `counter_if.sv` — DUT interface bundle
- `tb_counter_pkg.sv` — single package containing `counter_item`, `counter_sequence`, `counter_driver`, `counter_monitor`, `counter_scoreboard`, `counter_agent`, `counter_env`, and `counter_test`
- `tb_counter_uvm.sv` — top module instantiating DUT and launching UVM
- `files.f` — compile-order filelist for simulator or parser entry

## Using the example

From `examples/uvm_tb/`, point your simulator or analysis frontend at `files.f` so `counter_if.sv` is compiled before the package and top, and so Graphify sees the same deterministic ordering as a simulator:

```bash
vlog -f files.f
```

Any equivalent frontend can reuse the same order.

## Example analysis questions

- Can the tooling recover the UVM component hierarchy?
- Can it trace the virtual interface binding path?
- Can it identify the monitor → scoreboard analysis connection?
- Can it infer clock/reset and enable assumptions?
- Can it connect sequence intent to DUT-visible behavior?
