# src/insurance_analytics/utils/validation.py
from typing import Dict

REQUIRED_KEYS = {
    "data": ["data_dir", "raw_dir", "processed_dir"],
    "logs": ["logs_dir"],
    "reports": ["reports_dir", "plots_dir"],
    "models": ["models_dir"],
    "artifacts": ["artifacts_dir"],
}


def validate_config_structure(config: Dict) -> None:
    """
    Validate that required sections and keys exist in the config dict.

    Raises ValueError if a required key is missing.
    """
    if not isinstance(config, dict):
        raise ValueError("Config must be a mapping/dictionary.")

    for section, keys in REQUIRED_KEYS.items():
        section_data = config.get(section)
        if section_data is None:
            raise ValueError(f"Missing '{section}' section in data.yaml")

        if not isinstance(section_data, dict):
            raise ValueError(
                f"Expected '{section}' section to be a mapping (dict).")

        for key in keys:
            if key not in section_data:
                raise ValueError(f"Missing '{section}.{key}' in data.yaml")
