from pathlib import Path
from typing import Dict, Optional
from insurance_analytics.utils.project_root import get_project_root
from insurance_analytics.utils.validation import validate_config_structure
from insurance_analytics.core.config import load_config

# Default structure if keys are missing in config
DEFAULT_STRUCTURE = {
    "data": {
        "data_dir": "data",
        "raw_dir": "data/raw",
        "processed_dir": "data/processed",
    },
    "reports": {
        "reports_dir": "reports",
        "plots": "reports/plots",
    },
    
    "logs": {"logs_dir": "logs"},
    "models": {
        "model_dir": "src/insurance_analytics/models",
        "checkpoints": "src/insurance_analytics/models/checkpoints"
    },
    "artifacts": {"artifacts_dir": "artifacts"},
    "docs": {"docs_dir": "docs"},
    "notebooks": {"notebooks_dir": "notebooks"},
    "scripts": {"scripts_dir": "scripts"},
    "tests": {"tests_dir": "tests"},
}


class PathRegistry:
    """Read paths from config + defaults and resolve relative to root."""

    def __init__(self, root: Path, config: Optional[Dict] = None, create_dirs: bool = True):
        self.root = Path(root).resolve()
        self._create_dirs = create_dirs

        # Merge defaults with config
        merged_config = {}
        config = config or {}
        for section, defaults in DEFAULT_STRUCTURE.items():
            section_cfg = config.get(section, {})
            merged_section = dict(defaults)
            # YAML overwrites defaults if present
            merged_section.update(section_cfg)
            merged_config[section] = merged_section
        self.config = merged_config

        # Validate merged config
        validate_config_structure(self.config)

        # Create sections dynamically
        for section, keys in DEFAULT_STRUCTURE.items():
            setattr(self, section, self._init_section(
                section, self.config[section]))

    def _init_section(self, section: str, section_config: Dict[str, str]) -> Dict[str, Path]:
        """Resolve section paths and create directories."""
        container: Dict[str, Path] = {}
        for key, rel_path in section_config.items():
            path = (self.root / rel_path).resolve()
            if self._create_dirs:
                path.mkdir(parents=True, exist_ok=True)
            container[key] = path
        return container


class Settings:
    """Main settings object exposing path sections as properties."""

    def __init__(self, root: Optional[Path] = None, config: Optional[Dict] = None, create_dirs: bool = True):
        self.root = Path(root).resolve() if root else get_project_root()
        self.config = config or load_config()
        self.paths = PathRegistry(
            self.root, self.config, create_dirs=create_dirs)

    @property
    def DATA(self) -> Dict[str, Path]:
        return self.paths.data

    @property
    def LOGS(self) -> Dict[str, Path]:
        return self.paths.logs

    @property
    def REPORTS(self) -> Dict[str, Path]:
        return self.paths.reports  # reports_dir is inside data

    @property
    def MODELS(self) -> Dict[str, Path]:
        return self.paths.models

    @property
    def ARTIFACTS(self) -> Dict[str, Path]:
        return self.paths.artifacts

    @property
    def DOCS(self) -> Dict[str, Path]:
        return self.paths.docs

    @property
    def NOTEBOOKS(self) -> Dict[str, Path]:
        return self.paths.notebooks

    @property
    def SCRIPTS(self) -> Dict[str, Path]:
        return self.paths.scripts

    @property
    def TESTS(self) -> Dict[str, Path]:
        return self.paths.tests


# global settings instance
settings = Settings()
