"""
registry.py
------------
Manage project paths and global settings.

- Resolves paths from configuration.
- Creates directories if needed.
- Exposes convenient access to data, logs, models, and artifacts.
"""

from pathlib import Path
from typing import Dict, Optional
from insurance_analytics.utils.project_root import get_project_root
from insurance_analytics.core.config import load_config


class PathRegistry:
    """
    Builds and manages resolved project paths.

    Converts configuration entries into absolute Paths and optionally
    creates the directories on disk.

    Attributes
    ----------
    root : Path
        Base directory of the project.
    config : dict
        Loaded YAML configuration.
    data : dict
        Data-related paths.
    logs : dict
        Log directories.
    models : dict
        Model and checkpoint directories.
    artifacts : dict
        Artifact storage directories.
    """

    def __init__(self, root: Path, config: Dict, create_dirs: bool = True):
        self.root = root.resolve()
        self.config = config
        self._create_dirs = create_dirs

        self.data = self._paths_from_section(
            "data", ["data_dir", "raw_dir", "processed_dir", "reports_dir", "plots", "exports"])
        self.logs = self._paths_from_section("logs", ["logs_dir"])
        self.models = self._paths_from_section(
            "models", ["model_dir", "checkpoints"])
        self.artifacts = self._paths_from_section(
            "artifacts", ["artifacts_dir"])

    def _paths_from_section(self, section: str, keys: list[str]) -> Dict[str, Path]:
        """
        Convert a config section into a dictionary of resolved paths.

        Parameters
        ----------
        section : str
            Name of the configuration section.
        keys : list[str]
            Keys expected in the section.

        Returns
        -------
        dict
            Mapping of key -> resolved Path objects.
        """
        container = {}
        section_data = self.config.get(section, {})
        for key in keys:
            if key not in section_data:
                continue
            path = (self.root / section_data[key]).resolve()
            if self._create_dirs:
                path.mkdir(parents=True, exist_ok=True)
            container[key] = path
        return container


class Settings:
    """
    Main settings object.

    Loads configuration, validates structure, and exposes resolved paths
    through a PathRegistry. Can be used as a singleton via get_settings().
    """

    def __init__(self, root: Optional[Path] = None, config: Optional[Dict] = None, create_dirs: bool = True):
        self.root = root or get_project_root()
        self.config = config or load_config()
        self.paths = PathRegistry(
            self.root, self.config, create_dirs=create_dirs)

    @property
    def DATA(self) -> Dict[str, Path]:
        """Shortcut to data paths."""
        return self.paths.data

    @property
    def LOGS(self) -> Dict[str, Path]:
        """Shortcut to log paths."""
        return self.paths.logs

    @property
    def MODELS(self) -> Dict[str, Path]:
        """Shortcut to model paths."""
        return self.paths.models

    @property
    def ARTIFACTS(self) -> Dict[str, Path]:
        """Shortcut to artifact directories."""
        return self.paths.artifacts


# Singleton accessor
_SETTINGS_SINGLETON: Optional[Settings] = None


def get_settings(create_dirs: bool = True) -> Settings:
    """
    Returns a global Settings singleton.

    Parameters
    ----------
    create_dirs : bool
        If True, directories are created on disk.

    Returns
    -------
    Settings
        Global settings instance.
    """
    global _SETTINGS_SINGLETON
    if _SETTINGS_SINGLETON is None:
        _SETTINGS_SINGLETON = Settings(create_dirs=create_dirs)
    return _SETTINGS_SINGLETON
