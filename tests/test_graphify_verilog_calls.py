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


if __name__ == "__main__":
    unittest.main()
