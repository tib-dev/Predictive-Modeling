import tempfile
import unittest
from pathlib import Path
from unittest import mock

from insurance_analytics.core.registry import PathRegistry, Settings

# The config you provided (kept as a Python dict)
SAMPLE_CONFIG = {
    "data": {
        "data_dir": "data",
        "raw_dir": "data/raw",
        "interim_dir": "data/interim",
        "processed_dir": "data/processed",
        "postgres_exports_dir": "data/postgres_exports",
    },
    "logs": {"logs_dir": "logs"},
    "reports": {"reports_dir": "reports", "plots_dir": "plots"},
    "models": {"models_dir": "src/insurance_analytics/models"},
    "artifacts": {"artifacts_dir": "artifacts"},
}


class TestRegistryWithSampleConfig(unittest.TestCase):
    def setUp(self):
        # Temporary project root for each test
        self._tmpdir = tempfile.TemporaryDirectory()
        self.project_root = Path(self._tmpdir.name) / "project_root"
        self.project_root.mkdir(parents=True, exist_ok=True)

        # Patch validate_config_structure so tests don't depend on its implementation
        self._validate_patcher = mock.patch(
            "insurance_analytics.core.registry.validate_config_structure"
        )
        self.mock_validate = self._validate_patcher.start()

    def tearDown(self):
        self._validate_patcher.stop()
        self._tmpdir.cleanup()

    def test_all_paths_resolved_and_created(self):
        """Using SAMPLE_CONFIG -> every configured path should be resolved and directory created."""
        registry = PathRegistry(
            self.project_root, SAMPLE_CONFIG, create_dirs=True)

        # Data section keys
        for key, rel in SAMPLE_CONFIG["data"].items():
            self.assertIn(key, registry.data,
                          f"{key} missing from registry.data")
            expected = (self.project_root / rel).resolve()
            self.assertEqual(registry.data[key], expected)
            self.assertTrue(expected.exists() and expected.is_dir())

        # Logs
        self.assertIn("logs_dir", registry.logs)
        expected_logs = (self.project_root /
                         SAMPLE_CONFIG["logs"]["logs_dir"]).resolve()
        self.assertEqual(registry.logs["logs_dir"], expected_logs)
        self.assertTrue(expected_logs.exists() and expected_logs.is_dir())

        # Reports
        for key, rel in SAMPLE_CONFIG["reports"].items():
            self.assertIn(key, registry.reports)
            expected = (self.project_root / rel).resolve()
            self.assertEqual(registry.reports[key], expected)
            self.assertTrue(expected.exists() and expected.is_dir())

        # Models
        self.assertIn("models_dir", registry.models)
        expected_models = (self.project_root /
                           SAMPLE_CONFIG["models"]["models_dir"]).resolve()
        self.assertEqual(registry.models["models_dir"], expected_models)
        self.assertTrue(expected_models.exists() and expected_models.is_dir())

        # Artifacts
        self.assertIn("artifacts_dir", registry.artifacts)
        expected_artifacts = (
            self.project_root / SAMPLE_CONFIG["artifacts"]["artifacts_dir"]).resolve()
        self.assertEqual(
            registry.artifacts["artifacts_dir"], expected_artifacts)
        self.assertTrue(expected_artifacts.exists()
                        and expected_artifacts.is_dir())

    def test_no_creation_when_create_dirs_false(self):
        """When create_dirs=False, the Path objects should still resolve but directories shouldn't be created."""
        registry = PathRegistry(
            self.project_root, SAMPLE_CONFIG, create_dirs=False)

        # Pick a subset to verify (if this passes for one, others are same logic)
        expected_raw = (self.project_root /
                        SAMPLE_CONFIG["data"]["raw_dir"]).resolve()
        expected_models = (self.project_root /
                           SAMPLE_CONFIG["models"]["models_dir"]).resolve()

        self.assertEqual(registry.data["raw_dir"], expected_raw)
        self.assertEqual(registry.models["models_dir"], expected_models)

        self.assertFalse(expected_raw.exists(),
                         "data/raw should not exist when create_dirs=False")
        self.assertFalse(expected_models.exists(),
                         "models dir should not exist when create_dirs=False")

    def test_validate_config_structure_called_with_sample_config(self):
        _ = PathRegistry(self.project_root, SAMPLE_CONFIG, create_dirs=False)
        self.mock_validate.assert_called_once_with(SAMPLE_CONFIG)


class TestSettingsUsingSampleConfig(unittest.TestCase):
    def setUp(self):
        # prepare temp project root and patch get_project_root to return it
        self._tmpdir = tempfile.TemporaryDirectory()
        self.project_root = Path(self._tmpdir.name) / "root"
        self.project_root.mkdir(parents=True, exist_ok=True)

        self._validate_patcher = mock.patch(
            "insurance_analytics.core.registry.validate_config_structure"
        )
        self._validate_patcher.start()

        self._get_root_patcher = mock.patch(
            "insurance_analytics.core.registry.get_project_root", return_value=self.project_root
        )
        self.mock_get_root = self._get_root_patcher.start()

    def tearDown(self):
        self._get_root_patcher.stop()
        self._validate_patcher.stop()
        self._tmpdir.cleanup()

    def test_settings_exposes_properties_and_resolves_paths(self):
        settings = Settings(config=SAMPLE_CONFIG, create_dirs=True)

        # Ensure properties map to underlying PathRegistry dicts
        self.assertIs(settings.DATA, settings.paths.data)
        self.assertIs(settings.LOGS, settings.paths.logs)
        self.assertIs(settings.REPORTS, settings.paths.reports)
        self.assertIs(settings.MODELS, settings.paths.models)
        self.assertIs(settings.ARTIFACTS, settings.paths.artifacts)

        # Verify at least one entry per section is correct
        self.assertIn("data_dir", settings.DATA)
        self.assertEqual(settings.DATA["data_dir"],
                         (self.project_root / "data").resolve())

        self.assertIn("logs_dir", settings.LOGS)
        self.assertEqual(settings.LOGS["logs_dir"],
                         (self.project_root / "logs").resolve())

        self.assertIn("reports_dir", settings.REPORTS)
        self.assertEqual(
            settings.REPORTS["reports_dir"], (self.project_root / "reports").resolve())

        self.assertIn("models_dir", settings.MODELS)
        self.assertEqual(settings.MODELS["models_dir"], (
            self.project_root / "src/insurance_analytics/models").resolve())

        self.assertIn("artifacts_dir", settings.ARTIFACTS)
        self.assertEqual(
            settings.ARTIFACTS["artifacts_dir"], (self.project_root / "artifacts").resolve())


if __name__ == "__main__":
    unittest.main()
