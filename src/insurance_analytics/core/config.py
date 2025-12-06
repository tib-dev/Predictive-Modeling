from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)


def load_config(path: str | None = None) -> dict:
    """
    Load a YAML configuration file safely.
    If path is None, load from top-level configs folder.
    """
    if path is None:
        from insurance_analytics.utils.project_root import get_project_root
        path = get_project_root() / "configs" / "data.yaml"
    path = Path(path)

    try:
        if not path.exists():
            logger.error(f"Config file not found: {path.resolve()}")
            return {}

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            logger.error(f"Config root must be a dictionary: {path.resolve()}")
            return {}

        return data

    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error in {path.resolve()}: {e}")
        return {}

    except Exception as e:
        logger.error(f"Unexpected error loading config {path.resolve()}: {e}")
        return {}
