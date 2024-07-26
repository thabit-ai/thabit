import openai
import pandas as pd
import click
import json
import asyncio
import aiohttp
from colorama import Fore, Style, init
from datetime import datetime
import os
from rich.table import Table
from rich.console import Console
from rich.style import Style as RichStyle
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import textwrap
from tqdm import tqdm
from thabit.evaluators.eval import evaluate_output
from thabit.utils.llm import initialize_openai, call_ai_model
from thabit.utils.load import load_config

# Initialize colorama
init()

# Initialize rich console
console = Console()

# Main asynchronous function to run the evaluation


async def evaluate_models(config_file, data_file):
    config = load_config(config_file)
    data = pd.read_csv(data_file)
    results = []
    total_input_tokens = 0
    total_output_tokens = 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        for model in config["models"]:
            model_params = config["global_parameters"].copy()
            model_params.update(model)
            openai_params = initialize_openai(model_params)
            model_short_name = model["model_short_name"]

            for index, row in data.iterrows():
                task = asyncio.ensure_future(
                    call_ai_model(
                        session, model, model_short_name, row["context"], openai_params
                    )
                )
                tasks.append((model, row, task))

        progress_bar = tqdm(total=len(tasks), desc="Processing", unit="task")
        responses = await asyncio.gather(*[task for _, _, task in tasks])

        for (model, row, _), output in zip(tasks, responses):
            try:
                passed = evaluate_output(output, row[2], row[1])
                result = {
                    "Model": model["model_short_name"],
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

    return results, config


def format_results_for_display(results, config):
    context_output = {}
    for result in results:
        context = result["Context"]
        model = result["Model"]
        passed = result["Passed"]
        if context not in context_output:
            context_output[context] = {
                "Expected Output": result["Expected Output"],
                "Evaluation Method": result["Evaluation Method"],
            }
        context_output[context][model] = (passed, result["Output"])

    header = ["Context", "Expected Output", "Evaluation Method"] + [
        model["model_short_name"] for model in config["models"]
    ]
    table_data = [header]
    for context, values in context_output.items():
        wrapped_context = textwrap.fill(context, width=50)
        row = [wrapped_context, values["Expected Output"], values["Evaluation Method"]]
        for model in header[3:]:
            if model in values:
                passed, output = values[model]
                if passed == f"[red]✘[/red]":
                    row.append(f"{passed} [white on red]{output}[/white on red]")
                else:
                    row.append(passed)
            else:
                row.append("[red]✘[/red]")
        table_data.append(row)

    return header, table_data


def display_results(header, table_data):
    table = Table(title="Evaluation Results")
    for column in header:
        table.add_column(column)
    for row in table_data[1:]:
        table.add_row(*row)
    console.print(table)


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


def display_best_model(best_model, best_accuracy):
    centered_text = Text(justify="center")
    centered_text.append(f"🏆 ")
    centered_text.append(f"{best_model} ", style="bold green")
    centered_text.append(f"is the winner with ")
    centered_text.append(f"{best_accuracy:.2f}% ", style="bold green")
    centered_text.append(f"accuracy over the dataset 🏆")
    panel = Panel(
        centered_text,
        border_style="bold green",
        title="Winner",
        title_align="center",
        width=50,
    )
    centered_panel = Align.center(panel)
    console.print(centered_panel)


async def run_evaluation(config_file, data_file):
    results, config = await evaluate_models(config_file, data_file)
    header, table_data = format_results_for_display(results, config)
    display_results(header, table_data)
    best_model, best_accuracy = determine_best_model(results)
    display_best_model(best_model, best_accuracy)

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


# Function to visualize a specific evaluation
def visualize_evaluation(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)

    console.print(f"Global Parameters: {data['global_parameters']}")
    console.print("\nEvaluation Results:")
    for result in data["results"]:
        result["Passed"] = (
            f"[green]✔[/green]" if result["Passed"] == "✔" else f"[red]✘[/red]"
        )
    table = Table(title="Evaluation Results")
    headers = data["results"][0].keys()
    for header in headers:
        table.add_column(header)
    for result in data["results"]:
        row = [result.get(header, "") for header in headers]
        table.add_row(*row)
    console.print(table)


# Function to compare two evaluation runs
def compare_evaluations(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    results1 = data1["results"]
    results2 = data2["results"]

    comparison = []
    for res1, res2 in zip(results1, results2):
        if res1["Passed"] == res2["Passed"]:
            comparison.append(
                {
                    "Model": res1["Model"],
                    "Context": res1["Context"],
                    "Expected Output": res1["Expected Output"],
                    "Evaluation Method": res1["Evaluation Method"],
                    "Passed": res1["Passed"],
                }
            )
        else:
            comparison.append(
                {
                    "Model": res1["Model"],
                    "Context": res1["Context"],
                    "Expected Output": res1["Expected Output"],
                    "Evaluation Method": res1["Evaluation Method"],
                    "Passed": (
                        f"[green]✔[/green] => [red]✘[/red]"
                        if res1["Passed"] == "✔"
                        else f"[red]✘[/red] => [green]✔[/green]"
                    ),
                }
            )

    console.print(f"Evaluation 1 [{file1}]")
    console.print(f"Global Parameters: {data1['global_parameters']}")
    console.print(f"Evaluation 2 [{file2}]")
    console.print(f"Global Parameters: {data2['global_parameters']}")
    console.print("\nComparison Results:")
    table = Table(title="Comparison Results")
    headers = comparison[0].keys()
    for header in headers:
        table.add_column(header)
    for comp in comparison:
        row = [comp.get(header, "") for header in headers]
        table.add_row(*row)
    console.print(table)


# CLI interface using Click
@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--config", default="config.json", help="Path to the configuration JSON file."
)
@click.option("--data", default="data.csv", help="Path to the data CSV file.")
def run(config, data):
    asyncio.run(run_evaluation(config, data))


@cli.command()
@click.argument("file_name")
def visualize(file_name):
    visualize_evaluation(file_name)


@cli.command()
@click.argument("file1")
@click.argument("file2")
def compare(file1, file2):
    compare_evaluations(file1, file2)


if __name__ == "__main__":
    cli()
