module counter #(
  parameter int WIDTH = 4
) (
  input  logic             clk,
  input  logic             rst_n,
  input  logic             en,
  output logic [WIDTH-1:0] count,
  output logic             rollover
);

  logic [WIDTH-1:0] count_n;

  always_comb begin
    count_n = count;
    if (en) begin
      count_n = count + 1'b1;
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      count <= '0;
    end else begin
      count <= count_n;
    end
  end

  assign rollover = en && (count == {WIDTH{1'b1}});

endmodule
