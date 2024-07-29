import asyncio
import aiohttp
import pandas as pd
from thabit.utils.load import load_config
from thabit.utils.llm import initialize_openai, call_ai_model
from thabit.evaluators.eval import evaluate_output
from thabit.utils.cli import (
    format_results_for_display,
    display_results,
    display_best_model,
    display_accuracy_chart,
)
from thabit.utils.llm import determine_best_model
from tqdm import tqdm
from datetime import datetime
import os
import json
from rich.console import Console
from thabit.services.dataset import read_dataset
from thabit.utils.logger import get_logger

logger = get_logger()
console = Console()


# Main asynchronous function to run the evaluation
async def evaluate_models(config_data, dataset, models):
    # read dataset from dataset folder
    try:
        data = read_dataset(dataset)
        logger.info(f"Dataset: {data}")
    except Exception as e:
        logger.error(f"Error reading dataset: {e}")
        return
    results = []
    total_input_tokens = 0
    total_output_tokens = 0

    tasks = []
    for model in config_data["models"]:
        logger.debug(f"Models in running: {models}")
        logger.debug(f"Model in config: {model['model']}")
        if models and model["model"] not in models:
            # delete config data of model where model['model'] is not in models
            config_data["models"] = [
                m for m in config_data["models"] if m["model"] in models
            ]
            continue
        model_params = config_data["global_parameters"].copy()
        model_params.update(model)
        openai_params = initialize_openai(model_params)
        model_name = model["model_name"]

        for record in data["records"]:
            if record["prompt"] != "":
                prompt = record["prompt"]
            else:
                prompt = data["global_prompt"]
            context = record["context"]
            task = asyncio.ensure_future(
                call_ai_model(
                    model,
                    model_name,
                    prompt=prompt,
                    context=context,
                    openai_params=openai_params,
                )
            )
            tasks.append((model, record, task))

    progress_bar = tqdm(total=len(tasks), desc="Processing", unit="task")
    responses = await asyncio.gather(*[task for _, _, task in tasks])

    logger.info(f"Responses: {responses}")
    logger.info(f"Tasks: {tasks}")
    logger.info("Zip tasks and responses")
    logger.info(list(zip(tasks, responses)))
    for (model, record, _), output in zip(tasks, responses):
        try:
            passed = evaluate_output(
                output,
                expected_output=record["expected_output"],
                evaluation_method=record["evaluation_method"],
            )
            result = {
                "Model": model["model_name"],
                "Context": record["context"],
                "Output": output,
                "Expected Output": record["expected_output"],
                "Evaluation Method": record["evaluation_method"],
                "Passed": f"[green]✔[/green]" if passed else f"[red]✘[/red]",
            }
            results.append(result)
            total_input_tokens += len(record["context"].split())
            total_output_tokens += len(output.split())
            progress_bar.update(1)
            progress_bar.set_postfix(
                {
                    "Input Tokens": total_input_tokens,
                    "Output Tokens": total_output_tokens,
                }
            )
        except Exception as e:
            print(f"Error: {e}")

    progress_bar.close()

    return results, config_data


async def run_evaluation(config, dataset, models):
    results, config = await evaluate_models(config, dataset, models)
    header, table_data = format_results_for_display(results, config)
    display_results(header, table_data)
    display_accuracy_chart(header, table_data)

    # Save results to a JSON file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    output_file = f"eval-{timestamp}.json"
    os.makedirs("evals", exist_ok=True)
    os.makedirs(f"evals/{dataset}", exist_ok=True)
    with open(os.path.join(f"evals/{dataset}/", output_file), "w") as file:
        json.dump(
            {"global_parameters": config["global_parameters"], "results": results},
            file,
            indent=4,
        )
    console.print(f"Evaluation results saved to evals/{dataset}/{output_file}")
