from pathlib import Path
from typing import Dict, Optional
from insurance_analytics.utils.project_root import get_project_root
from insurance_analytics.utils.validation import validate_config_structure
from insurance_analytics.core.config import load_config


class PathRegistry:
    """
    Reads paths from the provided config and resolves them relative to root.
    Only creates directories for keys present in the config (no hard-coded defaults).
    """

    def __init__(self, root: Path, config: Dict, create_dirs: bool = True):
        self.root = root.resolve()
        self.config = config or {}
        self._create_dirs = create_dirs

        # validate early
        validate_config_structure(self.config)

        # sections expected by tests and code
        self.data = self._paths_from_section("data")
        self.logs = self._paths_from_section("logs")
        self.reports = self._paths_from_section("reports")
        self.models = self._paths_from_section("models")
        self.artifacts = self._paths_from_section("artifacts")
        self.docs = self._paths_from_section("docs")
        self.notebooks = self._paths_from_section("notebooks")
        self.scripts = self._paths_from_section("scripts")
        self.tests = self._paths_from_section("tests")

    def _paths_from_section(self, section: str) -> Dict[str, Path]:
        """
        Convert a config section (a dict of name -> relative path) into resolved Path objects.
        Only processes keys that exist in the config for that section.
        """
        container: Dict[str, Path] = {}
        section_data = self.config.get(section, {}) or {}

        # support legacy string value
        if isinstance(section_data, str):
            section_data = {f"{section}_dir": section_data}

        for key, rel_path in section_data.items():
            if not rel_path:
                continue
            path = (self.root / rel_path).resolve()
            if self._create_dirs:
                path.mkdir(parents=True, exist_ok=True)
            container[key] = path
        return container


class Settings:
    """
    Main settings object that loads config (from YAML if none provided)
    and exposes resolved paths.
    """

    def __init__(
        self, root: Optional[Path] = None, config: Optional[Dict] = None, create_dirs: bool = True
    ):
        self.root = (root or get_project_root()).resolve()
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
        return self.paths.reports

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
