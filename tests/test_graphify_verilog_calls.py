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


if __name__ == "__main__":
    unittest.main()
