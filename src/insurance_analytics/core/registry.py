from pathlib import Path
from insurance_analytics.utils.project_root import get_project_root
from insurance_analytics.core.config import load_config
from insurance_analytics.utils.validation import validate_config_structure


class PathRegistry:
    """Handles all path resolution and folder creation."""

    def __init__(self, root: Path, config: dict):
        self.root = root
        self.config = config

        # Create all sub-registries
        self.data = self._paths_from_section("data", [
            "data_dir",
            "raw_dir",
            "processed_dir",
            "reports_dir",
            "plots",
            "exports",
        ])

        self.logs = self._paths_from_section("logs", ["logs_dir"])
        self.models = self._paths_from_section(
            "models", ["model_dir", "checkpoints"])
        self.artifacts = self._paths_from_section(
            "artifacts", ["artifacts_dir"])

    def _paths_from_section(self, section: str, keys: list):
        container = {}

        if section not in self.config:
            return container   # optional section

        for key in keys:
            if key not in self.config[section]:
                continue  # optional keys allowed

            path = self.root / self.config[section][key]
            path.mkdir(parents=True, exist_ok=True)
            container[key] = path

        return container


class Settings:
    """Global settings & registry container."""

    def __init__(self):
        self.root = get_project_root()
        self.config = load_config()

        # validate structure
        validate_config_structure(self.config)

        # paths
        self.paths = PathRegistry(self.root, self.config)

    # convenience shortcuts
    @property
    def DATA(self): return self.paths.data

    @property
    def LOGS(self): return self.paths.logs

    @property
    def MODELS(self): return self.paths.models

    @property
    def ARTIFACTS(self): return self.paths.artifacts


# GLOBAL INSTANCE
settings = Settings()
