import json
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


if __name__ == "__main__":
    unittest.main()
