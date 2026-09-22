"""CLI for the transition-based workflow-net to DECLARE translator."""

import csv
import json
from enum import Enum
from pathlib import Path

import typer
from lxml import etree
from rich.console import Console

from src.declare_translator.dec_translator import translate_to_DEC
from src.utils.petri_parser import parse_wn_from_pnml

console = Console()
app = typer.Typer(help="Synthesize DECLARE specifications over workflow-net transition IDs.")


class OutputFormat(str, Enum):
    json = "json"
    csv = "csv"


def write_to_json(output, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)
        file.write("\n")


def write_to_csv(output, output_path):
    """Keep the existing two-column model-summary CSV format."""
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(output.items())


@app.command()
def export_wn(
    pnml_file: Path = typer.Option(..., exists=True, dir_okay=False, readable=True),
    output_path: Path = typer.Option(..., dir_okay=False),
):
    """Export the parsed workflow net; names are retained as metadata."""
    try:
        write_to_json(parse_wn_from_pnml(pnml_file), output_path)
    except (OSError, ValueError, etree.XMLSyntaxError) as exc:
        console.print(f"Error: {exc}", style="red", markup=False)
        raise typer.Exit(code=1) from exc
    console.print(f"Workflow net saved to {output_path}", markup=False)


@app.command()
def declare_synth(
    pnml_file: Path = typer.Option(..., exists=True, dir_okay=False, readable=True),
    output_format: OutputFormat = typer.Option(OutputFormat.json),
    output_path: Path = typer.Option(..., dir_okay=False),
):
    """Apply the three original rules using transition IDs as the alphabet."""
    try:
        workflow_net = parse_wn_from_pnml(pnml_file)
        output = translate_to_DEC(workflow_net, pnml_file.name)
        writer = write_to_json if output_format == OutputFormat.json else write_to_csv
        writer(output, output_path)
    except (OSError, ValueError, etree.XMLSyntaxError) as exc:
        console.print(f"Error: {exc}", style="red", markup=False)
        raise typer.Exit(code=1) from exc
    console.print(f"DECLARE specification saved to {output_path}", markup=False)


if __name__ == "__main__":
    app()
