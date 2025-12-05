import unittest
import tempfile
from pathlib import Path
import shutil
import os
import sys
from pathlib import Path

# add project src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


from insurance_analytics.core.registry import Settings
from insurance_analytics.core.config import load_config
from insurance_analytics.utils.project_root import get_project_root
from insurance_analytics.utils.validation import validate_config_structure


class TestRegistry(unittest.TestCase):
    def setUp(self):
        """
        Create a temporary project structure and override get_project_root
        for isolated testing.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "insurance_analytics"
        self.project_root.mkdir()

        # Create configs folder and data.yaml
        configs = self.project_root / "configs"
        configs.mkdir()

        config_yaml = """
data:
  data_dir: "data/"
  raw_dir: "data/raw/"
  processed_dir: "data/processed/"
  reports_dir: "reports/"
  plots: "plots/"
  exports: "exports/"

logs:
  logs_dir: "logs/"

models:
  model_dir: "models/"
  checkpoints: "models/checkpoints/"

artifacts:
  artifacts_dir: "artifacts/"
"""
        (configs / "data.yaml").write_text(config_yaml)

        # Monkeypatch get_project_root
        self._orig_get_root = get_project_root
        from insurance_analytics.utils import project_root
        project_root.get_project_root = lambda: self.project_root

        # Initialize Settings
        self.settings = Settings()

    def tearDown(self):
        # Restore original get_project_root
        from insurance_analytics.utils import project_root
        project_root.get_project_root = self._orig_get_root

        # Clean temporary directory
        self.temp_dir.cleanup()

    # --------------------------
    # Tests
    # --------------------------

    def test_project_root_detection(self):
        self.assertEqual(self.settings.root, self.project_root)
        self.assertTrue(self.settings.root.exists())

    def test_config_load(self):
        cfg = load_config()
        self.assertIn("data", cfg)
        self.assertIn("logs", cfg)

    def test_validate_config_structure_valid(self):
        # Should not raise
        validate_config_structure(self.settings.config)

    def test_required_config_keys_missing(self):
        cfg = {"data": {"data_dir": "data/"}, "logs": {}}
        with self.assertRaises(ValueError):
            validate_config_structure(cfg)

    def test_data_registry_paths_created(self):
        paths = self.settings.DATA
        for key in ["data_dir", "raw_dir", "processed_dir", "reports_dir", "plots", "exports"]:
            self.assertTrue(paths[key].exists())

    def test_logs_registry_paths_created(self):
        self.assertTrue(self.settings.LOGS["logs_dir"].exists())

    def test_models_registry_paths_created(self):
        models = self.settings.MODELS
        self.assertTrue(models["model_dir"].exists())
        self.assertTrue(models["checkpoints"].exists())

    def test_artifacts_registry_paths_created(self):
        self.assertTrue(self.settings.ARTIFACTS["artifacts_dir"].exists())

    def test_registry_access_shortcuts(self):
        self.assertIn("data_dir", self.settings.DATA)
        self.assertIn("logs_dir", self.settings.LOGS)

    def test_optional_sections_supported(self):
        # Rewrite config without optional sections
        config_yaml = """
data:
  data_dir: "data/"
  reports_dir: "reports/"
  plots: "plots/"

logs:
  logs_dir: "logs/"
"""
        config_path = self.project_root / "configs" / "data.yaml"
        config_path.write_text(config_yaml)

        settings = Settings()
        self.assertTrue(settings.DATA["data_dir"].exists())
        self.assertTrue(settings.LOGS["logs_dir"].exists())


if __name__ == "__main__":
    unittest.main()
