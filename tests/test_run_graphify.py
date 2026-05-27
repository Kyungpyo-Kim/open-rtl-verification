import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "run_graphify.py"


class RunGraphifyCliTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
