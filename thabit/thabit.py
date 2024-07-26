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
from thabit.services.evaluate import run_evaluation
from thabit.utils.cli import display_results, display_best_model
from thabit.utils.llm import determine_best_model
from thabit.utils.load import load_config

# Initialize colorama
init()

# Initialize rich console
console = Console()


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
def eval(config, data):
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
