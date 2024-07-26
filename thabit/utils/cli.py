import textwrap
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()


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
