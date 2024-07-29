import json
from thabit.utils.logger import get_logger
import dotenv
import os

logger = get_logger()


def load_config(file_path):
    """
    Load configuration from JSON file.
    """
    # get the path of the command line pwd
    path = os.path.join(os.getcwd(), ".env")
    dotenv.load_dotenv(path)

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            # replace env variables with actual values
            try:
                for model in data["models"]:
                    model["api_key"] = os.getenv(model["api_key_env_var"], None)
                    if model["api_key"] is None:
                        logger.error(
                            f"API key not found in environment variables: {model['api_key_env_var']}"
                        )
            except KeyError:
                logger.error(f"Models is missing in the config file")
                raise ValueError(f"Model is missing in the config file")
            return data
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Configuration file is not a valid JSON file: {file_path}")
        raise json.JSONDecodeError(
            f"Configuration file is not a valid JSON file: {file_path}",
            "Configuration file is not a valid JSON file",
            0,
        )


def validate_config(config):
    """
    Validate the configuration file.
    """
    required_global_keys = ["temperature", "max_tokens", "top_p"]
    if "global_parameters" not in config:
        logger.error("Configuration is missing 'global_parameters' key.")
        raise ValueError("Configuration is missing 'global_parameters' key.")

    for key in required_global_keys:
        if key not in config["global_parameters"]:
            logger.error(
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
        logger.error(
            "Configuration is missing 'models' key or it is not a valid array."
        )
        raise ValueError(
            "Configuration is missing 'models' key or it is not a valid array."
        )

    required_model_keys = [
        "provider",
        "model",
        "model_name",
        "endpoint",
        "api_key_env_var",
    ]
    for model in config["models"]:
        for key in required_model_keys:
            if key not in model:
                logger.error(f"Model is missing required key: {key} in the config file")
                raise ValueError(
                    f"Model is missing required key: {key} in the config file"
                )
    return True
