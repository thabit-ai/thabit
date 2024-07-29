import openai
import aiohttp
from thabit.utils.logger import get_logger

logger = get_logger()


# Initialize OpenAI API for each model
def initialize_openai(model_config):
    """
    Initialize OpenAI API for each model
    """
    logger.info(f"Initializing OpenAI API for {model_config['model_name']}")
    openai.api_key = model_config["api_key"]
    params = model_config.copy()
    del params["provider"]
    del params["model"]
    del params["endpoint"]
    del params["api_key"]
    del params["model_name"]
    del params["api_key_env_var"]
    return params


# Asynchronous function to call the AI model
async def call_ai_model(model, model_name, context, openai_params):
    logger.info(f"Calling {model_name} model")
    prompt = "You are a helpful AI assistant. I will ask you a question and I want you to return the direct answer without explaining. If the question is about a number, yes/no, or a simple true/false, return required value with no explanation."
    url = model["endpoint"]
    headers = {
        "Authorization": f"Bearer {model['api_key']}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model["model"],
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": context},
        ],
        **openai_params,
    }
    logger.debug(f"Sending request to {url} with headers {headers} and data {data}")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()
            logger.debug(f"Received response from {url}: {result}")
            return result["choices"][0]["message"]["content"].strip()


def determine_best_model(results):
    model_accuracy = {}
    for result in results:
        model = result["Model"]
        passed = 1 if result["Passed"] == f"[green]✔[/green]" else 0
        if model not in model_accuracy:
            model_accuracy[model] = {"total": 0, "passed": 0}
        model_accuracy[model]["total"] += 1
        model_accuracy[model]["passed"] += passed

    best_model = None
    best_accuracy = 0
    for model, stats in model_accuracy.items():
        accuracy = (stats["passed"] / stats["total"]) * 100
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model

    return best_model, best_accuracy
