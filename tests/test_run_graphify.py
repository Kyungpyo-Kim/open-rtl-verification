import argparse
import importlib.util
import json
import networkx as nx
from unittest import mock
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "run_graphify.py"


class RunGraphifyCliTest(unittest.TestCase):
    def _init_git_repo(self, repo_dir: Path) -> None:
        subprocess.run(["git", "init", repo_dir.name], cwd=repo_dir.parent, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True, capture_output=True, text=True)

    def test_manifest_only_collects_local_uvm_example_sources(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td) / "uvm_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "examples/uvm_tb",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("GRAPHIFY_SOURCE: vendor", completed.stdout)

            manifest_path = output_dir / "sources.json"
            self.assertTrue(manifest_path.exists())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_count"], 3)
            self.assertEqual(
                manifest["relative_sources"],
                [
                    "counter_if.sv",
                    "tb_counter_pkg.sv",
                    "tb_counter_uvm.sv",
                ],
            )
            self.assertIsNone(manifest["filelist"])

    def test_manifest_only_honors_uvm_filelist_and_prefers_vendored_graphify(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td) / "uvm_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "examples/uvm_tb",
                    "--filelist",
                    "files.f",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("GRAPHIFY_SOURCE: vendor", completed.stdout)

            manifest_path = output_dir / "sources.json"
            self.assertTrue(manifest_path.exists())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_count"], 4)
            self.assertEqual(
                manifest["relative_sources"],
                [
                    str((REPO_ROOT / "examples" / "rtl" / "counter.sv").resolve()),
                    "counter_if.sv",
                    "tb_counter_pkg.sv",
                    "tb_counter_uvm.sv",
                ],
            )
            self.assertEqual(manifest["filelist"], "files.f")

    def test_manifest_only_honors_nested_uppercase_f_filelists(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            source_dir = temp_root / "uvm"
            source_dir.mkdir()

            (source_dir / "rtl").mkdir()
            (source_dir / "tb").mkdir()
            (source_dir / "rtl" / "core.sv").write_text("module core; endmodule\n", encoding="utf-8")
            (source_dir / "tb" / "core_tb.sv").write_text("module core_tb; endmodule\n", encoding="utf-8")
            (source_dir / "nested.f").write_text("tb/core_tb.sv\n", encoding="utf-8")
            (source_dir / "top.f").write_text("rtl/core.sv\n-F nested.f\n", encoding="utf-8")

            output_dir = temp_root / "uvm_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(source_dir),
                    "--filelist",
                    "top.f",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads((output_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_count"], 2)
            self.assertEqual(manifest["relative_sources"], ["rtl/core.sv", "tb/core_tb.sv"])
            self.assertEqual(manifest["filelist"], "top.f")

    def test_manifest_only_honors_nested_filelists_with_tab_whitespace(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            source_dir = temp_root / "uvm"
            source_dir.mkdir()

            (source_dir / "rtl").mkdir()
            (source_dir / "tb").mkdir()
            (source_dir / "rtl" / "core.sv").write_text("module core; endmodule\n", encoding="utf-8")
            (source_dir / "tb" / "core_tb.sv").write_text("module core_tb; endmodule\n", encoding="utf-8")
            (source_dir / "nested.f").write_text("tb/core_tb.sv\n", encoding="utf-8")
            (source_dir / "top.f").write_text("rtl/core.sv\n-F\tnested.f\n", encoding="utf-8")

            output_dir = temp_root / "uvm_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(source_dir),
                    "--filelist",
                    "top.f",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads((output_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_count"], 2)
            self.assertEqual(manifest["relative_sources"], ["rtl/core.sv", "tb/core_tb.sv"])
            self.assertEqual(manifest["filelist"], "top.f")

    def test_manifest_only_stages_git_repo_and_honors_sparse_checkout(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            repo_dir = temp_root / "remote-source.git"
            self._init_git_repo(repo_dir)

            (repo_dir / "rtl").mkdir()
            (repo_dir / "tb").mkdir()
            (repo_dir / "rtl" / "core.sv").write_text("module core; endmodule\n", encoding="utf-8")
            (repo_dir / "tb" / "core_tb.sv").write_text("module core_tb; endmodule\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True, text=True)
            subprocess.run(["git", "commit", "-m", "seed repo"], cwd=repo_dir, check=True, capture_output=True, text=True)

            output_dir = temp_root / "remote_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(repo_dir),
                    "--repo-ref",
                    "HEAD",
                    "--sparse-path",
                    "rtl",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                    "--staging-root",
                    str(temp_root / "staging"),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads((output_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_count"], 1)
            self.assertEqual(manifest["relative_sources"], ["rtl/core.sv"])
            self.assertEqual(manifest["repo_ref"], "HEAD")
            self.assertEqual(manifest["repo_url"], str(repo_dir))

    def test_manifest_only_accepts_named_open_target_preset(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td) / "ibex_manifest"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--target",
                    "ibex_rtl",
                    "--manifest-only",
                    "--output-dir",
                    str(output_dir),
                    "--staging-root",
                    str(Path(td) / "staging"),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads((output_dir / "sources.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["repo_url"], "https://github.com/lowRISC/ibex.git")
            self.assertEqual(manifest["repo_ref"], "master")
            self.assertTrue(all(path.startswith("rtl/") for path in manifest["relative_sources"]))

    def test_apply_open_target_defaults_uses_opentitan_preset_values(self):
        spec = importlib.util.spec_from_file_location("run_graphify", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        run_graphify = importlib.util.module_from_spec(spec)
        sys.modules["run_graphify"] = run_graphify
        spec.loader.exec_module(run_graphify)

        args = argparse.Namespace(
            input=None,
            target="opentitan_uart_dv",
            output_dir="graph/graphify_outputs/latest",
            repo_ref="HEAD",
            sparse_path=[],
        )

        try:
            updated = run_graphify.apply_open_target_defaults(args)
        finally:
            sys.modules.pop("run_graphify", None)

        self.assertEqual(updated.input, "https://github.com/lowRISC/opentitan.git")
        self.assertEqual(updated.output_dir, "graph/graphify_outputs/opentitan_uart_dv")
        self.assertEqual(updated.repo_ref, "master")
        self.assertEqual(updated.sparse_path, ["hw/ip/uart", "hw/dv/sv"])

    def test_apply_open_target_defaults_keeps_explicit_cli_overrides(self):
        spec = importlib.util.spec_from_file_location("run_graphify", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        run_graphify = importlib.util.module_from_spec(spec)
        sys.modules["run_graphify"] = run_graphify
        spec.loader.exec_module(run_graphify)

        args = argparse.Namespace(
            input="examples/uvm_tb",
            target="opentitan_uart_dv",
            output_dir="graph/graphify_outputs/custom_target",
            repo_ref="feature-branch",
            sparse_path=["custom/path"],
        )

        try:
            updated = run_graphify.apply_open_target_defaults(args)
        finally:
            sys.modules.pop("run_graphify", None)

        self.assertEqual(updated.input, "examples/uvm_tb")
        self.assertEqual(updated.output_dir, "graph/graphify_outputs/custom_target")
        self.assertEqual(updated.repo_ref, "feature-branch")
        self.assertEqual(updated.sparse_path, ["custom/path"])

    def test_open_target_config_entries_are_unique_and_complete(self):
        config = json.loads((REPO_ROOT / "configs" / "open_targets.json").read_text(encoding="utf-8"))
        targets = config["targets"]

        self.assertGreaterEqual(len(targets), 1)

        names = [target["name"] for target in targets]
        self.assertEqual(len(names), len(set(names)))

        for target in targets:
            self.assertTrue(target["name"])
            self.assertTrue(target["description"])
            self.assertTrue(target["repo_url"].startswith("https://github.com/"))
            self.assertTrue(target["repo_ref"])
            self.assertTrue(target["output_dir"].startswith("graph/graphify_outputs/"))
            self.assertIsInstance(target["sparse_paths"], list)
            self.assertGreaterEqual(len(target["sparse_paths"]), 1)
            self.assertTrue(all(path and not path.startswith("/") for path in target["sparse_paths"]))

    def test_cli_reports_unknown_open_target(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--target",
                "does_not_exist",
                "--manifest-only",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 1)
        self.assertIn("OPEN_TARGET_NOT_FOUND", completed.stderr)

    def test_render_graph_png_returns_error_when_graph_html_is_missing(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td)

            spec = importlib.util.spec_from_file_location("run_graphify", SCRIPT)
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            run_graphify = importlib.util.module_from_spec(spec)
            sys.modules["run_graphify"] = run_graphify
            spec.loader.exec_module(run_graphify)

            try:
                rc = run_graphify.render_graph_png(output_dir)
            finally:
                sys.modules.pop("run_graphify", None)

            self.assertEqual(rc, 1)

    def test_render_graph_png_invokes_helper_script(self):
        with tempfile.TemporaryDirectory() as td:
            output_dir = Path(td)
            (output_dir / "graph.html").write_text("<html></html>\n", encoding="utf-8")

            spec = importlib.util.spec_from_file_location("run_graphify", SCRIPT)
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            run_graphify = importlib.util.module_from_spec(spec)
            sys.modules["run_graphify"] = run_graphify
            spec.loader.exec_module(run_graphify)

            with mock.patch.object(run_graphify.subprocess, "run") as mocked_run:
                mocked_run.return_value = mock.Mock(returncode=0)

                try:
                    rc = run_graphify.render_graph_png(output_dir)
                finally:
                    sys.modules.pop("run_graphify", None)

            self.assertEqual(rc, 0)
            mocked_run.assert_called_once_with(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "render_html_to_png.py"),
                    str(output_dir / "graph.html"),
                    "--output",
                    str(output_dir / "graph.png"),
                ],
                check=False,
            )

    def test_filter_graph_by_confidence_view_keeps_only_extracted_edges(self):
        spec = importlib.util.spec_from_file_location("run_graphify", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        run_graphify = importlib.util.module_from_spec(spec)
        sys.modules["run_graphify"] = run_graphify
        spec.loader.exec_module(run_graphify)

        graph = nx.DiGraph()
        graph.add_node("keep")
        graph.add_node("keep_target")
        graph.add_node("drop")
        graph.add_node("drop_target")
        graph.add_edge("keep", "keep_target", confidence="EXTRACTED")
        graph.add_edge("drop", "drop_target", confidence="INFERRED")

        try:
            filtered = run_graphify.filter_graph_by_confidence_view(graph, "extracted")
        finally:
            sys.modules.pop("run_graphify", None)

        self.assertTrue(filtered.has_edge("keep", "keep_target"))
        self.assertFalse(filtered.has_edge("drop", "drop_target"))
        self.assertNotIn("drop", filtered.nodes)
        self.assertNotIn("drop_target", filtered.nodes)


if __name__ == "__main__":
    unittest.main()
