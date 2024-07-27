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

console = Console()


# Main asynchronous function to run the evaluation
async def evaluate_models(config_data, data):
    data = pd.read_csv(data)
    results = []
    total_input_tokens = 0
    total_output_tokens = 0

    tasks = []
    for model in config_data["models"]:
        model_params = config_data["global_parameters"].copy()
        model_params.update(model)
        openai_params = initialize_openai(model_params)
        model_name = model["model_name"]

        for index, row in data.iterrows():
            task = asyncio.ensure_future(
                call_ai_model(model, model_name, row["context"], openai_params)
            )
            tasks.append((model, row, task))

    progress_bar = tqdm(total=len(tasks), desc="Processing", unit="task")
    responses = await asyncio.gather(*[task for _, _, task in tasks])

    for (model, row, _), output in zip(tasks, responses):
        try:
            passed = evaluate_output(output, row[2], row[1])
            result = {
                "Model": model["model_name"],
                "Context": row[0],
                "Output": output,
                "Expected Output": row[2],
                "Evaluation Method": row[1],
                "Passed": f"[green]✔[/green]" if passed else f"[red]✘[/red]",
            }
            results.append(result)
            total_input_tokens += len(row["context"].split())
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


async def run_evaluation(config, data_file):
    results, config = await evaluate_models(config, data_file)
    header, table_data = format_results_for_display(results, config)
    display_results(header, table_data)
    display_accuracy_chart(header, table_data)

    # Save results to a JSON file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    output_file = f"eval-{timestamp}.json"
    os.makedirs("evals", exist_ok=True)
    with open(os.path.join("evals", output_file), "w") as file:
        json.dump(
            {"global_parameters": config["global_parameters"], "results": results},
            file,
            indent=4,
        )
    console.print(f"Evaluation results saved to evals/{output_file}")
