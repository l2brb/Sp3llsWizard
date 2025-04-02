import os
import json
import csv
import typer
from rich import print
from rich.console import Console

from src.utils import petri_parser
from src.declare_translator import dec_translator 



app = typer.Typer(
    help="""
Welocme to Sp3llsWizard, a tool for synthesizing DECLARE specifications from safe and sound Workflow net casting three spells.
"""
)
console = Console()


def write_to_json(output, output_path: str):
    with open(output_path, 'w') as file:
        json.dump(output, file, indent=4)
    console.log(f"[green]Output JSON saved in[/green] {output_path}")


def write_to_csv(constraints, output_path: str):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in constraints.items():
            writer.writerow([key, value])
    console.log(f"[green]CSV saved in[/green] {output_path}")

@app.command()
def export_wn(
    pnml_file: str = typer.Option(..., help="File path .pnml"),
    output_path: str = typer.Option(..., help="File path WF.json")
):
    """
    Export WF net to JSON.
    """
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file)
    if workflow_net:
        from src.utils import wn_json  
        wn_json.write_to_json(workflow_net, output_path)
        console.print("[bold green]WF net succesfully exported![/bold green]")
    else:
        console.print("[bold red]Error in WN parsing.[/bold red]")

@app.command()
def run_algorithm(
    pnml_file: str = typer.Option(..., help="File path .pnml"),
    output_format: str = typer.Option("json", help="Output format: 'json' o 'csv'"),
    output_path: str = typer.Option(..., help="output file path")
):
    """
    Cast the three spells and save output to csv or json
    """
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file)
    if not workflow_net:
        console.print("[bold red]Error in WN parsing[/bold red]")
        raise typer.Exit()

    model_name = os.path.basename(pnml_file)
    console.print(f"[cyan]DECLARE Synthesizing {model_name}...[/cyan]")

    output = dec_translator.translate_to_DEC(workflow_net, model_name)
    console.print("[bold green]DECLARE Constraints generated succesfully.[/bold green]")

    if output_format.lower() == "json":
        write_to_json(output, output_path)
    elif output_format.lower() == "csv":
        write_to_csv(output, output_path)
    else:
        console.print("[bold red]Invalid output format. Use 'json' or 'csv'.[/bold red]")


if __name__ == "__main__":
    app()
