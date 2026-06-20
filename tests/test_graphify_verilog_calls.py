import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "vendor" / "graphify").resolve()))

from graphify.extract import extract, extract_verilog


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
  child u_child (.in_sig(a & b), .out_sig(tmp));
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
        self.assertIn(("b", "u_child.in_sig"), binds_port_edges)
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
  child u_child(a & b, b, y);
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
        self.assertIn(("b", "u_child.in_a"), binds_port_edges)
        self.assertIn(("b", "u_child.in_b"), binds_port_edges)
        self.assertIn(("y", "u_child.out_y"), binds_port_edges)

    def test_extracts_condition_signal_dependencies_from_procedural_assignments(self):
        source = """
module condition_demo(input logic sel, input logic a, input logic b, output logic y);
  always_comb begin
    if (sel)
      y = a;
    else
      y = b;
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "condition_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("sel", "y"), assign_edges)
        self.assertIn(("a", "y"), assign_edges)
        self.assertIn(("b", "y"), assign_edges)

    def test_ignores_numeric_literal_artifacts_in_case_assignments(self):
        source = """
module case_demo(input logic sel, input logic a, input logic b, output logic y);
  always_comb begin
    case (sel)
      1'b0: y = a;
      default: y = b;
    endcase
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "case_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("sel", "y"), assign_edges)
        self.assertIn(("a", "y"), assign_edges)
        self.assertIn(("b", "y"), assign_edges)
        self.assertNotIn(("b0", "y"), assign_edges)

    def test_uses_base_signal_for_indexed_assignment_lhs(self):
        source = """
module indexed_demo(input logic [1:0] sel, input logic a, output logic y);
  logic [3:0] mem;

  always_comb begin
    mem[sel] = a;
    y = mem[sel];
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "indexed_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("sel", "mem"), assign_edges)
        self.assertIn(("a", "mem"), assign_edges)
        self.assertIn(("mem", "y"), assign_edges)
        self.assertIn(("sel", "y"), assign_edges)
        self.assertNotIn(("a", "sel"), assign_edges)
        self.assertNotIn(("mem", "sel"), assign_edges)

    def test_extracts_procedural_assignments_inside_for_loops(self):
        source = """
module loop_demo(input logic [1:0] in, output logic [1:0] out);
  integer i;

  always_comb begin
    for (i = 0; i < 2; i++)
      out[i] = in[i];
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "loop_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("in", "out"), assign_edges)
        self.assertNotIn(("out", "i"), assign_edges)
        self.assertNotIn(("in", "i"), assign_edges)

    def test_extracts_procedural_assignments_inside_while_loops(self):
        source = """
module while_demo(input logic cond, input logic a, output logic y);
  always_comb begin
    while (cond)
      y = a;
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "while_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("cond", "y"), assign_edges)
        self.assertIn(("a", "y"), assign_edges)
        self.assertNotIn(("y", "cond"), assign_edges)

    def test_extracts_procedural_assignments_inside_repeat_loops_without_keyword_noise(self):
        source = """
module repeat_demo(input logic a, output logic y);
  always_comb begin
    repeat (2)
      y = a;
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "repeat_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("a", "y"), assign_edges)
        self.assertNotIn(("repeat", "y"), assign_edges)

    def test_extracts_procedural_assignments_inside_foreach_loops_without_index_noise(self):
        source = """
module foreach_demo(input logic [1:0] a, output logic [1:0] y);
  always_comb begin
    foreach (a[i])
      y[i] = a[i];
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "foreach_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("a", "y"), assign_edges)
        self.assertNotIn(("i", "y"), assign_edges)
        self.assertNotIn(("a", "i"), assign_edges)

    def test_extracts_procedural_assignments_inside_do_while_loops_without_keyword_noise(self):
        source = """
module do_demo(input logic cond, input logic a, output logic y);
  always_comb begin
    do
      y = a;
    while (cond);
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "do_demo.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        assign_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "assigns_to"
        }

        self.assertIn(("a", "y"), assign_edges)
        self.assertNotIn(("do", "y"), assign_edges)


    def test_extracts_uvm_class_hierarchy_and_methods_from_package(self):
        source = """
package demo_pkg;
  import uvm_pkg::*;

  class demo_item extends uvm_sequence_item;
    function new(string name = "demo_item");
      super.new(name);
    endfunction
  endclass

  class demo_test extends uvm_test;
    function void build_phase(uvm_phase phase);
      demo_item item;
      super.build_phase(phase);
      item = demo_item::type_id::create("item");
    endfunction
  endclass
endpackage
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "demo_pkg.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        contains_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "contains"
        }
        inherits_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "inherits"
        }
        package_symbol_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "uses_package_symbol"
        }

        self.assertIn(("demo_pkg", "demo_item"), contains_edges)
        self.assertIn(("demo_pkg", "demo_test"), contains_edges)
        self.assertIn(("demo_test", "build_phase()"), contains_edges)
        self.assertIn(("demo_item", "new()"), contains_edges)
        self.assertIn(("demo_item", "uvm_sequence_item"), inherits_edges)
        self.assertIn(("demo_test", "uvm_test"), inherits_edges)
        self.assertIn(("build_phase()", "demo_item::type_id"), package_symbol_edges)

    def test_does_not_duplicate_uvm_package_methods_at_file_scope(self):
        source = """
package demo_pkg;
  class demo_test;
    function void helper();
    endfunction

    function void build_phase();
      helper();
    endfunction
  endclass
endpackage
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "demo_pkg.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        helper_nodes = [node_id for node_id, label in labels.items() if label == "helper()"]
        build_phase_nodes = [node_id for node_id, label in labels.items() if label == "build_phase()"]
        contains_edges = [
            (edge["source"], edge["target"])
            for edge in result["edges"]
            if edge["relation"] == "contains"
        ]
        call_edges = [
            (edge["source"], edge["target"])
            for edge in result["edges"]
            if edge["relation"] == "calls"
        ]

        self.assertEqual(len(helper_nodes), 1)
        self.assertEqual(len(build_phase_nodes), 1)
        self.assertIn(
            next(node_id for node_id, label in labels.items() if label == "demo_test"),
            {source for source, _target in contains_edges},
        )
        self.assertIn((build_phase_nodes[0], helper_nodes[0]), call_edges)
        self.assertFalse(any(labels[source] == "demo_pkg.sv" and target in set(helper_nodes + build_phase_nodes) for source, target in contains_edges))

    def test_extracts_complex_uvm_package_example_class_structure(self):
        result = extract_verilog(Path("examples/uvm_tb/tb_counter_pkg.sv"))

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        contains_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "contains"
        }
        inherits_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "inherits"
        }

        self.assertIn(("tb_counter_pkg", "counter_driver"), contains_edges)
        self.assertIn(("tb_counter_pkg", "counter_env"), contains_edges)
        self.assertIn(("tb_counter_pkg", "counter_test"), contains_edges)
        self.assertIn(("counter_driver", "build_phase()"), contains_edges)
        self.assertIn(("counter_env", "connect_phase()"), contains_edges)
        self.assertIn(("counter_test", "run_phase"), contains_edges)
        self.assertIn(("counter_test", "uvm_test"), inherits_edges)

    def test_extracts_basic_uvm_config_and_tlm_adapters(self):
        source = """
package demo_pkg;
  class demo_driver extends uvm_driver;
    virtual demo_if vif;

    function void build_phase(uvm_phase phase);
      if (!uvm_config_db#(virtual demo_if)::get(this, "", "vif", vif)) begin
      end
    endfunction
  endclass

  class demo_agent extends uvm_component;
    function void connect_phase(uvm_phase phase);
      driver.seq_item_port.connect(sequencer.seq_item_export);
      monitor.ap.connect(scoreboard.analysis_export);
    endfunction
  endclass
endpackage
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "demo_pkg.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        config_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "uvm_config_get"
        }
        typed_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "typed_as"
        }
        connect_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "connects_to"
        }

        self.assertIn(("build_phase()", "config::vif"), config_edges)
        self.assertIn(("config::vif", "virtual demo_if"), typed_edges)
        self.assertIn(("driver.seq_item_port", "sequencer.seq_item_export"), connect_edges)
        self.assertIn(("monitor.ap", "scoreboard.analysis_export"), connect_edges)

    def test_extracts_uvm_sequence_start_and_run_test_adapters(self):
        source = """
package demo_pkg;
  class demo_test extends uvm_test;
    task run_phase(uvm_phase phase);
      seq.start(env.agent.sequencer);
    endtask
  endclass
endpackage

module demo_top;
  initial begin
    run_test("demo_test");
  end
endmodule
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "demo_top.sv"
            path.write_text(source, encoding="utf-8")
            result = extract([path])

        labels = {node["id"]: node["label"] for node in result["nodes"]}
        start_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "starts_on"
        }
        run_test_edges = {
            (labels[edge["source"]], labels[edge["target"]])
            for edge in result["edges"]
            if edge["relation"] == "runs_test"
        }

        self.assertIn(("seq", "env.agent.sequencer"), start_edges)
        self.assertIn(("demo_top", "demo_test"), run_test_edges)


if __name__ == "__main__":
    unittest.main()
