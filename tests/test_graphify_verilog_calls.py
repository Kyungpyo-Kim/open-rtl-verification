import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "vendor" / "graphify").resolve()))

from graphify.extract import extract


class GraphifyVerilogCallExtractionTest(unittest.TestCase):
    def test_extracts_local_function_and_task_calls_without_keyword_noise(self):
        source = """
module helper_demo;
  function automatic int leaf;
    return 1;
  endfunction

  function automatic int mid;
    if (1) begin
      return leaf();
    end
    return leaf();
  endfunction

  task automatic top_task;
    int value;
    value = mid();
  endtask
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "helper_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        call_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "calls"
        }

        self.assertIn(("mid()", "leaf()"), call_edges)
        self.assertIn(("top_task", "mid()"), call_edges)
        self.assertNotIn(("mid()", "if"), call_edges)

    def test_extracts_function_calls_with_parameters(self):
        source = """
module param_demo;
  function automatic int add;
    input int a;
    input int b;
    return a + b;
  endfunction

  function automatic int calc;
    input int x;
    input int y;
    return add(x, y);
  endfunction

  task automatic top_task;
    int result;
    result = calc(3, 4);
  endtask
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "param_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        call_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "calls"
        }

        self.assertIn(("calc()", "add()"), call_edges)
        self.assertIn(("top_task", "calc()"), call_edges)

    def test_extracts_package_qualified_symbol_uses_in_local_scope(self):
        source = """
module pkg_demo;
  import ibex_pkg::*;

  function automatic ibex_pkg::alu_op_t decode;
    return ibex_pkg::ALU_ADD;
  endfunction

  task automatic top_task;
    ibex_pkg::csr_num_e csr_num;
    csr_num = ibex_pkg::CSR_MSTATUS;
  endtask
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pkg_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        package_symbol_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "uses_package_symbol"
        }

        self.assertIn(("decode()", "ibex_pkg::alu_op_t"), package_symbol_edges)
        self.assertIn(("decode()", "ibex_pkg::ALU_ADD"), package_symbol_edges)
        self.assertIn(("top_task", "ibex_pkg::csr_num_e"), package_symbol_edges)
        self.assertIn(("top_task", "ibex_pkg::CSR_MSTATUS"), package_symbol_edges)
        self.assertNotIn(("pkg_demo", "ibex_pkg::*"), package_symbol_edges)

    def test_extracts_simple_assign_signal_dependencies(self):
        source = """
module signal_demo;
  logic src_a;
  logic src_b;
  logic dst;

  assign dst = src_a & src_b;
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "signal_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        signal_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("src_a", "dst"), signal_edges)
        self.assertIn(("src_b", "dst"), signal_edges)

    def test_extracts_basic_signal_connectivity_from_assigns_and_port_bindings(self):
        source = """
module child(input logic in_sig, output logic out_sig);
endmodule

module top(input logic a, input logic b, output logic y);
  logic tmp;
  child u_child (.in_sig(a), .out_sig(tmp));
  assign y = tmp & b;
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "connectivity_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        binds_port_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "binds_port"
        }
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("a", "u_child.in_sig"), binds_port_edges)
        self.assertIn(("tmp", "u_child.out_sig"), binds_port_edges)
        self.assertIn(("tmp", "y"), assign_edges)
        self.assertIn(("b", "y"), assign_edges)

    def test_extracts_simple_procedural_signal_dependencies_without_confusing_declarations(self):
        source = """
module procedural_demo(input logic a, input logic b, output logic y);
  logic tmp = 1'b0;

  always_comb begin
    tmp = a & b;
    y <= tmp;
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "procedural_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("a", "tmp"), assign_edges)
        self.assertIn(("b", "tmp"), assign_edges)
        self.assertIn(("tmp", "y"), assign_edges)
        self.assertNotIn(("logic", "tmp"), assign_edges)

    def test_extracts_basic_signal_connectivity_from_positional_port_bindings(self):
        source = """
module child(input logic in_a, input logic in_b, output logic out_y);
endmodule

module top(input logic a, input logic b, output logic y);
  child u_child(a, b, y);
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "connectivity_positional_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        binds_port_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "binds_port"
        }

        self.assertIn(("a", "u_child.in_a"), binds_port_edges)
        self.assertIn(("b", "u_child.in_b"), binds_port_edges)
        self.assertIn(("y", "u_child.out_y"), binds_port_edges)


if __name__ == "__main__":
    unittest.main()
