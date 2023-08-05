"""Command line interface for YamlTable.

See https://docs.python.org/3/using/cmdline.html#cmdoption-m for why module is
named __main__.py.
"""


import pathlib
import pprint
from typing import List, Optional, Tuple

import typer

import yamltable
from yamltable.typing import ExitCode, FileArg, Row, Schema, StatusColor


app = typer.Typer(
    help=(
        "Utility for working with YAML files organized similar to a relational"
        " database table."
    )
)


@app.command(name="index")
def index_(index: int, file_path: pathlib.Path = FileArg) -> None:
    """Get row at INDEX in FILE_PATH."""

    rows, _ = load_data(file_path)

    try:
        row = rows[index]
    except IndexError:
        typer.secho(
            f"Error: Index {index} is out of bounds.",
            fg=StatusColor.ERROR.value,
            err=True,
        )
        raise typer.Exit(code=ExitCode.ERROR.value)
    else:
        typer.secho(pprint.pformat(row, indent=2))


@app.command(name="list")
def list_(key: str, file_path: pathlib.Path = FileArg) -> None:
    """List all dictionary KEY values in FILE_PATH."""

    rows, _ = load_data(file_path)

    for idx, row in enumerate(rows):
        try:
            typer.secho(row[key])
        except KeyError:
            typer.secho(
                f"Error: Row {idx} does not have key {key}.",
                fg=StatusColor.ERROR.value,
                err=True,
            )
            raise typer.Exit(code=ExitCode.ERROR.value)


def load_data(file_path: pathlib.Path) -> Tuple[List[Row], Optional[Schema]]:
    """Attempt to load data from YAML file.

    Args:
        file_path: YAML file path

    Returns:
        YAML row data, YAML schema
    """

    try:
        return yamltable.read(file_path)
    except (FileNotFoundError, TypeError) as xcpt:
        typer.secho(f"Error: {xcpt}", fg=StatusColor.ERROR.value, err=True)
        raise typer.Exit(code=ExitCode.ERROR.value)


@app.command()
def search(key: str, value: str, file_path: pathlib.Path = FileArg) -> None:
    """Search dictionaries in FILE_PATH with matching KEY and VALUE pairs."""

    rows, _ = load_data(file_path)
    matches = yamltable.search(key, value, rows)

    if matches:
        for match in yamltable.search(key, value, rows):
            typer.secho(pprint.pformat(match, indent=2))
    else:
        typer.secho(
            f"No rows found with (key={key}, value={value}) pair.",
            fg=StatusColor.EMPTY.value,
        )


@app.command()
def sort(key: str, file_path: pathlib.Path = FileArg) -> None:
    """Sort dictionaries in FILE_PATH by KEY values."""

    rows, schema = load_data(file_path)

    try:
        sorted_rows = yamltable.sort(key, rows)
    except TypeError as xcpt:
        typer.secho(f"Error: {xcpt}", fg=StatusColor.ERROR.value, err=True)
        raise typer.Exit(code=ExitCode.ERROR.value)
    else:
        yamltable.write(file_path, sorted_rows, schema)


@app.command()
def validate(file_path: pathlib.Path = FileArg) -> None:
    """Check that every dictionary in FILE_PATH has conforms to its schema."""

    rows, schema = load_data(file_path)
    valid, row, msg = yamltable.validate(rows, schema)

    if valid:
        typer.secho(
            "YAML file rows conform to its schema.",
            fg=StatusColor.SUCCESS.value,
        )
    elif row == -1:
        typer.secho(
            f"Invalid schema: {msg}", fg=StatusColor.ERROR.value, err=True
        )
        raise typer.Exit(code=ExitCode.ERROR.value)
    else:
        typer.secho(
            f"Invalid row {row}: {msg}", fg=StatusColor.ERROR.value, err=True
        )
        raise typer.Exit(code=ExitCode.INVALID.value)


@app.command()
def version() -> None:
    """Display application version."""

    typer.secho(f"yamltable {yamltable.__version__}")


if __name__ == "__main__":  # pragma: no cover
    app()
