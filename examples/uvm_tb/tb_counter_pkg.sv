package tb_counter_pkg;
  import uvm_pkg::*;
  `include "uvm_macros.svh"

  class counter_item extends uvm_sequence_item;
    rand bit en;
         bit [3:0] observed_count;
         bit       observed_rollover;

    `uvm_object_utils_begin(counter_item)
      `uvm_field_int(en, UVM_DEFAULT)
      `uvm_field_int(observed_count, UVM_DEFAULT)
      `uvm_field_int(observed_rollover, UVM_DEFAULT)
    `uvm_object_utils_end

    function new(string name = "counter_item");
      super.new(name);
    endfunction
  endclass

  class counter_sequence extends uvm_sequence #(counter_item);
    `uvm_object_utils(counter_sequence)

    function new(string name = "counter_sequence");
      super.new(name);
    endfunction

    task body();
      counter_item req;
      repeat (16) begin
        req = counter_item::type_id::create("req");
        start_item(req);
        req.en = 1'b1;
        finish_item(req);
      end

      req = counter_item::type_id::create("idle_req");
      start_item(req);
      req.en = 1'b0;
      finish_item(req);
    endtask
  endclass

  class counter_driver extends uvm_driver #(counter_item);
    `uvm_component_utils(counter_driver)

    virtual counter_if vif;

    function new(string name = "counter_driver", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if (!uvm_config_db#(virtual counter_if)::get(this, "", "vif", vif)) begin
        `uvm_fatal("NOVIF", "counter_driver requires vif")
      end
    endfunction

    task run_phase(uvm_phase phase);
      counter_item req;

      vif.rst_n <= 1'b0;
      vif.en    <= 1'b0;
      repeat (2) @(posedge vif.clk);
      vif.rst_n <= 1'b1;

      forever begin
        seq_item_port.get_next_item(req);
        @(posedge vif.clk);
        vif.en <= req.en;
        seq_item_port.item_done();
      end
    endtask
  endclass

  class counter_monitor extends uvm_component;
    `uvm_component_utils(counter_monitor)

    virtual counter_if vif;
    uvm_analysis_port #(counter_item) ap;

    function new(string name = "counter_monitor", uvm_component parent = null);
      super.new(name, parent);
      ap = new("ap", this);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      if (!uvm_config_db#(virtual counter_if)::get(this, "", "vif", vif)) begin
        `uvm_fatal("NOVIF", "counter_monitor requires vif")
      end
    endfunction

    task run_phase(uvm_phase phase);
      counter_item sample;
      forever begin
        @(posedge vif.clk);
        sample = counter_item::type_id::create("sample");
        sample.en                = vif.en;
        sample.observed_count    = vif.count;
        sample.observed_rollover = vif.rollover;
        ap.write(sample);
      end
    endtask
  endclass

  class counter_scoreboard extends uvm_subscriber #(counter_item);
    `uvm_component_utils(counter_scoreboard)

    bit [3:0] expected_count;

    function new(string name = "counter_scoreboard", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void write(counter_item t);
      if (!t.en) begin
        return;
      end

      expected_count = expected_count + 1'b1;
      if (t.observed_count !== expected_count) begin
        `uvm_error("COUNT_MISMATCH",
          $sformatf("expected=%0d observed=%0d", expected_count, t.observed_count))
      end
    endfunction
  endclass

  class counter_agent extends uvm_component;
    `uvm_component_utils(counter_agent)

    uvm_sequencer #(counter_item) sequencer;
    counter_driver                driver;
    counter_monitor               monitor;

    function new(string name = "counter_agent", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      sequencer = uvm_sequencer#(counter_item)::type_id::create("sequencer", this);
      driver    = counter_driver::type_id::create("driver", this);
      monitor   = counter_monitor::type_id::create("monitor", this);
    endfunction

    function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
      driver.seq_item_port.connect(sequencer.seq_item_export);
    endfunction
  endclass

  class counter_env extends uvm_component;
    `uvm_component_utils(counter_env)

    counter_agent      agent;
    counter_scoreboard scoreboard;

    function new(string name = "counter_env", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      agent      = counter_agent::type_id::create("agent", this);
      scoreboard = counter_scoreboard::type_id::create("scoreboard", this);
    endfunction

    function void connect_phase(uvm_phase phase);
      super.connect_phase(phase);
      agent.monitor.ap.connect(scoreboard.analysis_export);
    endfunction
  endclass

  class counter_test extends uvm_test;
    `uvm_component_utils(counter_test)

    counter_env env;
    virtual counter_if vif;

    function new(string name = "counter_test", uvm_component parent = null);
      super.new(name, parent);
    endfunction

    function void build_phase(uvm_phase phase);
      super.build_phase(phase);
      env = counter_env::type_id::create("env", this);

      if (!uvm_config_db#(virtual counter_if)::get(this, "", "vif", vif)) begin
        `uvm_fatal("NOVIF", "counter_test requires vif")
      end

      uvm_config_db#(virtual counter_if)::set(this, "env.agent.*", "vif", vif);
    endfunction

    task run_phase(uvm_phase phase);
      counter_sequence seq;
      phase.raise_objection(this);
      seq = counter_sequence::type_id::create("seq");
      seq.start(env.agent.sequencer);
      repeat (2) @(posedge vif.clk);
      phase.drop_objection(this);
    endtask
  endclass

endpackage
