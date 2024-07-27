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

# Initialize colorama
init()

# Initialize rich console
console = Console()


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
    webbrowser.open(url)
    console.print(f"[green]Opened config route in web browser: {url}[/green]")
    app.run(debug=True, port=3300)


if __name__ == "__main__":
    cli()
