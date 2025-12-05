def validate_config_structure(cfg: dict):
    required = {
        "data": ["data_dir", "reports_dir", "plots"],
        "logs": ["logs_dir"],
    }

    for section, keys in required.items():
        if section not in cfg:
            raise ValueError(f"Missing '{section}' in data.yaml")

        for key in keys:
            if key not in cfg[section]:
                raise ValueError(f"Missing '{section}.{key}' in data.yaml")
