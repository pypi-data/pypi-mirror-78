"""Command line interface for sorting YAML files."""


import pathlib
from typing import Any, IO, Iterable, List, Optional, Sequence, Tuple, Union

import jsonschema
from jsonschema import exceptions
import yaml

from yamltable.typing import Row, Schema


__author__ = "Macklan Weinstein"
__version__ = "0.1.4"


def dependencies(unsorted: Sequence[Row], depends: str, name: str) -> List[Row]:
    """Sort rows based on the dependencies found in key.

    Args:
        unsorted: Rows to sort.
        depends: Dictionary key whose values are other dictionary dependencies.
        name: Foreign key for dependencies.

    Raises:
        ValueError: If rows contain circular requirements.

    Returns:
        Rows sorted by requirements.
    """

    sorted_: List[Row] = []
    while unsorted:
        # Find rows containing only dependencies in sorted_.
        names = [pkg[name] for pkg in sorted_]
        rows = [
            (idx, pkg)
            for idx, pkg in enumerate(unsorted)
            if set(pkg[depends]).issubset(names)
        ]

        if rows:
            idxs, pkgs = zip(*rows)
            # Append found rows to sorted_ and remove them from unsorted.
            sorted_ += pkgs
            unsorted = [
                elem for idx, elem in enumerate(unsorted) if idx not in idxs
            ]
        else:
            # If no rows are found then there exist circular dependencies.
            raise ValueError("encountered circular dependencies.")

    return sorted_


def read(
    stream: Union[IO[str], pathlib.Path, str]
) -> Tuple[List[Row], Optional[Schema]]:
    """Read data from YAML file.

    Args:
        stream: YAML text, text I/O stream, or file path.

    Raises:
        FileNotFoundError: If unable to find file path.
        TypeError: If file is not organized as a list.

    Returns:
        YAML data.
    """

    if isinstance(stream, pathlib.Path):
        stream = stream.read_text()

    try:
        data = yaml.safe_load(stream)
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as xcpt:
        raise TypeError(f"invalid YAML file: {xcpt}")

    if isinstance(data, list):
        return data, None
    elif isinstance(data, dict):
        try:
            return data["rows"], data["schema"]
        except KeyError:
            raise TypeError(
                "YAML file does not have a schema and rows organization"
            )
    else:
        raise TypeError("YAML file is not organized in a tabular format")


def search(key: str, val: Any, rows: Iterable[Row]) -> List[Row]:
    """Search dictionaries by key and value.

    Args:
        key: Search key.
        val: Key comparison value.
        rows: Dictionaries to search.

    Returns:
        Matching dictionaries.

    Examples:
        >>> rows = [{"foo": 1, "bar": 2}, {"foo": 5, "bar": 6}]
        >>> search("bar", 6, rows)
        [{'foo': 5, 'bar': 6}]
    """

    return [row for row in rows if key in row and row[key] == val]


def sort(key: str, rows: Iterable[Row]) -> List[Row]:
    """Sort dictionaries based on value for supplied key name.

    Args:
        key: Search key.
        rows: Dictionaries to sort.

    Returns:
        List of sorted dictionaries.

    Examples:
        >>> rows = [{"foo": 5, "bar": 2}, {"foo": 3, "bar": 6}]
        >>> sort("foo", rows)
        [{'foo': 3, 'bar': 6}, {'foo': 5, 'bar': 2}]
        >>> sort("bar", rows)
        [{'foo': 5, 'bar': 2}, {'foo': 3, 'bar': 6}]
    """

    return sorted(rows, key=lambda row: row[key])


def validate(
    rows: Iterable[Row], schema: Optional[Schema]
) -> Tuple[bool, int, str]:
    """Check that each row satisfies the schema.

    Args:
        rows: Dictionaries to validate.
        schema: JSON schema for validation.

    Returns:
        Whether all rows are valid, invalid row index or -1,
            invalid error message.
    """

    try:
        jsonschema.Draft7Validator.check_schema(schema)
    except (exceptions.SchemaError, exceptions.UnknownType) as xcpt:
        error_msg = str(xcpt)
        return False, -1, error_msg

    validator = jsonschema.Draft7Validator(schema)
    for idx, row in enumerate(rows):
        try:
            validator.validate(row)
        except exceptions.ValidationError as xcpt:
            error_msg = str(xcpt)
            return False, idx, error_msg

    return True, -1, ""


def write(
    file_path: pathlib.Path,
    rows: List[Row],
    schema: Optional[Schema] = None,
    sort_keys: bool = False,
) -> None:
    """Write data to YAML file.

    Args:
        file_path: YAML file path.
        rows: List of dictionaries to write.
        schema: JSON schema dictionary.
        sort_keys: Whether to sort row keys.
    """

    if schema is None:
        with open(file_path, "w") as handle:
            yaml.dump(rows, handle, sort_keys=sort_keys)
    else:
        data = {"schema": schema, "rows": rows}
        with open(file_path, "w") as handle:
            yaml.dump(data, handle, sort_keys=sort_keys)
