import json
from thabit.utils.logger import get_logger

logger = get_logger()


def load_config(file_path):
    """
    Load configuration from JSON file.
    """
    current_logger = logger.bind(function="load_config")
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        current_logger.error(f"Configuration file not found: {file_path}")
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError:
        current_logger.error(
            f"Configuration file is not a valid JSON file: {file_path}"
        )
        raise json.JSONDecodeError(
            f"Configuration file is not a valid JSON file: {file_path}",
            "Configuration file is not a valid JSON file",
            0,
        )


def validate_config(config):
    """
    Validate the configuration file.
    """
    current_logger = logger.bind(function="validate_config")
    required_global_keys = ["temperature", "max_tokens", "top_p"]
    if "global_parameters" not in config:
        current_logger.error("Configuration is missing 'global_parameters' key.")
        raise ValueError("Configuration is missing 'global_parameters' key.")

    for key in required_global_keys:
        if key not in config["global_parameters"]:
            current_logger.error(
                f"'global_parameters' is missing required key: {key} in the config file"
            )
            raise ValueError(
                f"'global_parameters' is missing required key: {key} in the config file"
            )

    if (
        "models" not in config
        or not isinstance(config["models"], list)
        or len(config["models"]) == 0
    ):
        current_logger.error(
            "Configuration is missing 'models' key or it is not a valid array."
        )
        raise ValueError(
            "Configuration is missing 'models' key or it is not a valid array."
        )

    required_model_keys = [
        "provider",
        "model",
        "model_short_name",
        "endpoint",
        "api_key",
    ]
    for model in config["models"]:
        for key in required_model_keys:
            if key not in model:
                current_logger.error(
                    f"Model is missing required key: {key} in the config file"
                )
                raise ValueError(
                    f"Model is missing required key: {key} in the config file"
                )
    return True
