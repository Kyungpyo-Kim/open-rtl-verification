`timescale 1ns/1ps

module tb_counter_uvm;

  import uvm_pkg::*;
  import tb_counter_pkg::*;

  localparam int WIDTH = 4;

  logic clk;
  counter_if #(WIDTH) cif(clk);

  counter #(
    .WIDTH(WIDTH)
  ) dut (
    .clk      (clk),
    .rst_n    (cif.rst_n),
    .en       (cif.en),
    .count    (cif.count),
    .rollover (cif.rollover)
  );

  always #5 clk = ~clk;

  initial begin
    clk = 1'b0;
    uvm_config_db#(virtual counter_if)::set(null, "uvm_test_top", "vif", cif);
    run_test("counter_test");
  end

endmodule
