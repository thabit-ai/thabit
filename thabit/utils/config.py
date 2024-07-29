from thabit.utils.logger import get_logger

logger = get_logger()


def get_all_models(config):
    models = []
    for model in config.get("models", []):
        models.append(model.get("model"))
    logger.debug(f"All models: {models}")
    return models


def has_models(models, config):
    logger.debug(f"Models to check: {models}")
    # check if config has all the models in the list as 'model_name'
    all_models = get_all_models(config)
    logger.debug(f"All models: {all_models}")
    models = [model.strip() for model in models.split(",")]
    for model in models:
        if model not in all_models:
            logger.error(f"Model {model} not found in config.")
            raise ValueError(f"Model {model} not found in config.")
    return True
