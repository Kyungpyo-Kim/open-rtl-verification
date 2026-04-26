`timescale 1ns/1ps

module tb_counter;

  localparam int WIDTH = 4;

  logic             clk;
  logic             rst_n;
  logic             en;
  logic [WIDTH-1:0] count;
  logic             rollover;

  counter #(
    .WIDTH(WIDTH)
  ) dut (
    .clk      (clk),
    .rst_n    (rst_n),
    .en       (en),
    .count    (count),
    .rollover (rollover)
  );

  always #5 clk = ~clk;

  initial begin
    clk  = 1'b0;
    rst_n = 1'b0;
    en   = 1'b0;

    repeat (2) @(posedge clk);
    rst_n = 1'b1;

    repeat (3) @(posedge clk);
    en = 1'b1;

    repeat (15) @(posedge clk);
    en = 1'b0;

    @(posedge clk);
    $finish;
  end

endmodule
