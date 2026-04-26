from pathlib import Path
from typing import Annotated

import typer


app = typer.Typer()


@app.command()
def main(
    input_path: Annotated[Path, typer.Option("--input", help="Input file path.")],
    output_path: Annotated[Path, typer.Option("--output", help="Output file path.")],
) -> None:
    typer.echo(f"Input: {input_path}")
    typer.echo(f"Output: {output_path}")
