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
from thabit.utils.load import load_config, validate_config
from thabit.services.evaluate import run_evaluation
from thabit.utils.cli import display_results, display_best_model, display_accuracy_chart
from thabit.utils.llm import determine_best_model
from thabit.utils.load import load_config
from flask import Flask, request, jsonify
from thabit.routes.ui import app
import webbrowser
import threading
import time
from thabit.utils.cli import show_main_menu

# Initialize colorama
init()

# Initialize rich console
console = Console()


# CLI interface using Click
@click.group(invoke_without_command=True)
@click.option("--show-menu", is_flag=True, help="Show the main menu.")
@click.pass_context
def cli(ctx, show_menu):
    if ctx.invoked_subcommand is None or show_menu:
        show_main_menu()
        # list all available commands and their descriptions and options
        console.print("[bold][blue]Available commands:[/blue][/bold]")
        for command in cli.commands:
            console.print(f"[bold]{command}[/bold]")
            console.print(f"    [italic]{cli.commands[command].__doc__}[/italic]")
            # list all options for the command
            for option in cli.commands[command].params:
                console.print(f"        [green]--{option.name}[/green]")


@cli.command()
@click.option(
    "--config", default="config.json", help="Path to the configuration JSON file."
)
@click.option("--dataset", required=True, help="Path to the dataset folder.")
def eval(config, data):
    """Evaluate LLMs using your own dataset."""
    try:
        # load config data
        config = load_config(config)
        # validate config data
        if validate_config(config):
            # run evaluation
            asyncio.run(run_evaluation(config, data))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        exit(1)


@cli.command()
@click.option(
    "--config_path", default="config.json", help="Path to the configuration JSON file."
)
def config(config_path):
    """Open the /config route in a web browser."""
    url = f"http://127.0.0.1:3300/config?config_path={config_path}"

    def run_app():
        app.run(debug=False, port=3300, use_reloader=False)

    # Run the Flask app in a separate thread
    threading.Thread(target=run_app).start()

    # Give the server a second to start up
    time.sleep(1)

    console.print(f"[green]Opened config route in web browser: {url}[/green]")
    webbrowser.open(url)


# Create/Edit dataset
@cli.command()
@click.option("--dataset", required=True, help="Path to the dataset folder.")
@click.option("--version", help="Version of the dataset.")
def dataset(dataset, version):
    """Open the /dataset route in a web browser."""
    url = f"http://127.0.0.1:3300/dataset?dataset={dataset}&version={version}"

    def run_app():
        app.run(debug=False, port=3300, use_reloader=False)

    # Run the Flask app in a separate thread
    threading.Thread(target=run_app).start()

    # Give the server a second to start up
    time.sleep(1)

    console.print(f"[green]Opened dataset route in web browser: {url}[/green]")
    webbrowser.open(url)


if __name__ == "__main__":
    cli()
