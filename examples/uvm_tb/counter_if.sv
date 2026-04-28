interface counter_if #(parameter int WIDTH = 4) (input logic clk);
  logic             rst_n;
  logic             en;
  logic [WIDTH-1:0] count;
  logic             rollover;
endinterface
