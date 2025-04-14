import os
import json
import csv
import typer
import pyfiglet
from rich import print
from rich.console import Console
from rich.progress import Progress

from src.utils import petri_parser
from src.declare_translator import dec_translator 
from src.declare_translator import dec_translator_silent


console = Console()

app = typer.Typer(
    help="""
Welcome to Sp3llsWizard, a tool for synthesizing DECLARE specifications from safe and sound Workflow net casting three spells.
"""
)
# ascii_banner = pyfiglet.figlet_format("Sp3llsWizard")
# console.print(ascii_banner, style="blue")


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
    Export the parsed Workflow net into a JSON file.
    """
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file)
    if workflow_net:
        from src.utils import wn_json  
        wn_json.write_to_json(workflow_net, output_path)
        console.print("[bold green]WF net succesfully exported![/bold green]")
    else:
        console.print("[bold red]Error in WN parsing.[/bold red]")

@app.command()
def declare_synth(
    pnml_file: str = typer.Option(..., help="File path .pnml"),
    output_format: str = typer.Option("json", help="Output format: 'json' o 'csv'"),
    output_path: str = typer.Option(..., help="output file path")
):
    """
    Cast the three spells and save output to CSV or JSON.
    """
    with Progress() as progress:
        # Parsing PNML File
        parse_task = progress.add_task("[cyan]Parsing PNML file...", total=1)
        workflow_net = petri_parser.parse_wn_from_pnml(pnml_file)
        progress.update(parse_task, advance=1)

        if not workflow_net:
            console.print("[bold red]Error in WN parsing[/bold red]")
            raise typer.Exit()

        # DECLARE Synthesizer
        synth_task = progress.add_task("[cyan]Synthesizing DECLARE constraints...", total=1)
        model_name = os.path.basename(pnml_file)
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        progress.update(synth_task, advance=1)

    console.print("[bold green]DECLARE Constraints generated succesfully.[/bold green]")

    if output_format.lower() == "json":
        write_to_json(output, output_path)
    elif output_format.lower() == "csv":
        write_to_csv(output, output_path)
    else:
        console.print("[bold red]Invalid output format. Use 'json' or 'csv'.[/bold red]")



@app.command()
def declare_silent_synth(
    pnml_file: str = typer.Option(..., help="File path .pnml"),
    output_format: str = typer.Option("json", help="Output format: 'json' o 'csv'"),
    output_path: str = typer.Option(..., help="output file path")
):
    """
    Cast the three (+ 1) spells and save output to CSV or JSON.
    This algorithm removes the silent transitions eventually present in the input model.
    """
    with Progress() as progress:
        # Parsing PNML File
        parse_task = progress.add_task("[cyan]Parsing PNML file...", total=1)
        workflow_net = petri_parser.parse_wn_from_pnml(pnml_file)
        progress.update(parse_task, advance=1)

        if not workflow_net:
            console.print("[bold red]Error in WN parsing[/bold red]")
            raise typer.Exit()

        # DECLARE Synthesizer
        synth_task = progress.add_task("[cyan]Synthesizing DECLARE constraints...", total=1)
        model_name = os.path.basename(pnml_file)
        output = dec_translator_silent.translate_to_DEC(workflow_net, model_name)
        progress.update(synth_task, advance=1)

    console.print("[bold green]DECLARE Constraints generated succesfully.[/bold green]")

    if output_format.lower() == "json":
        write_to_json(output, output_path)
    elif output_format.lower() == "csv":
        write_to_csv(output, output_path)
    else:
        console.print("[bold red]Invalid output format. Use 'json' or 'csv'.[/bold red]")

if __name__ == "__main__":
    app()
