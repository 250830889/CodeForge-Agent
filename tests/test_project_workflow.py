from pathlib import Path
import unittest

from codeforge_agent.audit import AuditLogger
from codeforge_agent.project_profile import inspect_project
from codeforge_agent.verifier import verify_project


class ProjectWorkflowTests(unittest.TestCase):
    def test_profile_detects_python_project(self) -> None:
        # TemporaryDirectory keeps each test independent on every platform.
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            (tmp_path / "pyproject.toml").write_text("[project]\nname = 'demo'\nversion = '0.1.0'\n")
            profile = inspect_project(tmp_path)
            self.assertEqual(profile.manifest, "pyproject.toml")
            self.assertIn("Python", profile.languages)

    def test_verifier_compiles_python_project(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            (tmp_path / "pyproject.toml").write_text("[project]\nname = 'demo'\nversion = '0.1.0'\n")
            (tmp_path / "module.py").write_text("value = 1\n")
            _, results = verify_project(tmp_path)
            self.assertTrue(results)
            self.assertTrue(all(result.returncode == 0 for result in results))

    def test_audit_writes_jsonl(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            logger = AuditLogger("demo", tmp_path)
            logger.record("tool_finished", tool="read_file", ok=True)
            self.assertIn('"event": "tool_finished"', (tmp_path / "demo.jsonl").read_text())
