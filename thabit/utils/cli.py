import textwrap
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from thabit.utils.logger import get_logger

console = Console()
logger = get_logger()


def format_results_for_display(results, config):
    context_output = {}

    logger.debug(f"Formatting results for display with the following data: {results}")
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
        model["model_name"] for model in config["models"]
    ]
    logger.debug(f"Header for the table: {header}")
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
    logger.debug(
        f"Displaying results with the following data: {header} and {table_data}"
    )
    table = Table(title="Evaluation Results")
    for column in header:
        table.add_column(column)
    for row in table_data[1:]:
        table.add_row(*row)
    console.print(table)


def display_accuracy_chart(header, table_data):
    # read table data and create the accuracy percentage for
    # each model, in a dict called model_accuracies
    model_accuracies = {}
    for row in table_data[1:]:
        for i, model in enumerate(header[3:]):
            if model not in model_accuracies:
                model_accuracies[model] = {"correct": 0, "total": 0}
            if row[i + 3] == f"[green]✔[/green]":
                model_accuracies[model]["correct"] += 1
            model_accuracies[model]["total"] += 1

    # Calculate accuracy percentage for each model
    for model, data in model_accuracies.items():
        accuracy = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0
        model_accuracies[model] = accuracy

    max_bar_length = 40
    bar_char = "█"

    # Sort the data in descending order based on values
    sorted_data = sorted(
        model_accuracies.items(), key=lambda item: item[1], reverse=True
    )

    # Create the bar chart as a list of Text objects
    bar_chart = []
    max_value = max(model_accuracies.values())
    for i, (model, value) in enumerate(sorted_data):
        bar_length = int(value / max_value * max_bar_length)
        bar = bar_char * bar_length
        if i == 0 or value == max_value:
            # Top one(s) in green
            bar_style = "bold green"
        else:
            # Others in faded green
            bar_style = "light_salmon3"
        # ensure that bar_text has the same length of the max model name
        max_model_name_length = max([len(model) for model in model_accuracies.keys()])
        bar_text = Text(
            f"{model: <{max_model_name_length}} | {bar} {value}%", style=bar_style
        )
        bar_chart.append(bar_text)

    # Combine the bar chart into a single Text object
    bar_chart_text = Text("\n\n").join(bar_chart)

    # Create a Panel to display the bar chart
    panel = Panel(
        bar_chart_text,
        title="Model Evaluation Accuracy",
        # border_style="blue",
        padding=(2, 2),
    )

    # Render the panel to the console
    console.print(panel)


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


def show_main_menu():
    """show the main menu"""
    thabit_ascii = """
████████╗██╗  ██╗ █████╗ ██████╗ ██╗████████╗
╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██║╚══██╔══╝
   ██║   ███████║███████║██████╔╝██║   ██║
   ██║   ██╔══██║██╔══██║██╔══██╗██║   ██║
   ██║   ██║  ██║██║  ██║██████╔╝██║   ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝
    """
    description = """
    Thabit is a platform to evaluate multiple LLMs at once using your own dataset.
    """

    console.print("[deep_sky_blue1]" + thabit_ascii + "[/deep_sky_blue1]")
    console.print("[bold][blue]" + description + "[/blue][/bold]")
