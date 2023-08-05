"""Library types for YamlTable."""


import enum
from typing import Any, Dict

import typer

Row = Dict[str, Any]
Schema = Dict[str, Any]


class ExitCode(enum.Enum):
    """Exit code statuses."""

    SUCCESS = 0
    INVALID = 1
    ERROR = 2


FileArg = typer.Argument(
    ..., dir_okay=False, exists=True, file_okay=True, resolve_path=True
)


class StatusColor(enum.Enum):
    """Colors for message types."""

    EMPTY = typer.colors.YELLOW
    ERROR = typer.colors.RED
    SUCCESS = typer.colors.BRIGHT_GREEN
