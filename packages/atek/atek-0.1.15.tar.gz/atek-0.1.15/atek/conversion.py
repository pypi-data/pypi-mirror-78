from typing import *
from toolz.curried import pipe, take, map, merge
import itertools as it
from functools import singledispatch
import pandas as pd

__all__ = ["to_table", "transpose"]

@singledispatch
def to_table(data: Iterable[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """Conversion function that takes either a
        pandas DataFrame,
        Iterable of Dicts,
        dict,
        or string
    and converts it into an iterator (generator) of records where each record
    is a dict with keys of type str and values of type Any.

    >>> data = [
    ...     {"fname": "Axl", "lname": "Rose", "Band": "Guns 'n' Roses"},
    ...     {"fname": "Angus", "lname": "Young", "Band": "AC/DC"},
    ...     {"fname": "Steven", "lname": "Tyler", "Band": "Aerosmith"},
    ... ]
    # Returns an iterator (generator)
    >>> to_table(data)
    <generator object to_table at 0x10c101eb0>
    # Use list to visualize the data
    >>> list(to_table(data))
    [
        {'fname': 'Axl', 'lname': 'Rose', 'Band': "Guns 'n' Roses"},
        {'fname': 'Angus', 'lname': 'Young', 'Band': 'AC/DC'},
        {'fname': 'Steven', 'lname': 'Tyler', 'Band': 'Aerosmith'}
    ]
    >>> list(to_table(data[0]))
    [
        {'column': 'fname', 'value': 'Axl'},
        {'column': 'lname', 'value': 'Rose'},
        {'column': 'Band', 'value': "Guns 'n' Roses"}
    ]
    >>> list(to_table("Axl Rose"))
    [{'value': 'Axl Rose'}]
    >>> df = pd.DataFrame.from_records(data)
    >>> df
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> list(to_table(df))
    [
        {'fname': 'Axl', 'lname': 'Rose', 'Band': "Guns 'n' Roses"},
        {'fname': 'Angus', 'lname': 'Young', 'Band': 'AC/DC'},
        {'fname': 'Steven', 'lname': 'Tyler', 'Band': 'Aerosmith'}
    ]
    """
    for row in data:
        yield row


@to_table.register(dict)
def _(data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    for k, v in data.items():
        yield {"column": k, "value": v}


@to_table.register(str)
def _(data: str) -> Iterator[Dict[str, Any]]:
    yield {"value": data}


@to_table.register(pd.DataFrame)
def _(data: pd.DataFrame) -> Iterator[Dict[str, Any]]:
    for row in data.to_dict("records"):
        yield row


@singledispatch
def transpose(data: Iterable[Dict[str, Any]], limit: int=3
    ) -> Iterable[Dict[str,Any]]:
    """Transposes a table (list of dicts) such that columns are
    rows and rows are columns.

    from atek.conversion import *
    >>> import pandas as pd
    >>> data = [
    ...     {"fname": "Axl", "lname": "Rose", "Band": "Guns 'n' Roses"},
    ...     {"fname": "Angus", "lname": "Young", "Band": "AC/DC"},
    ...     {"fname": "Steven", "lname": "Tyler", "Band": "Aerosmith"},
    ... ]
    >>> list(transpose(data))
    [
        {'column': 'fname', 'row 1': 'Axl', 'row 2': 'Angus', 'row 3': 'Steven'},
        {'column': 'lname', 'row 1': 'Rose', 'row 2': 'Young', 'row 3': 'Tyler'},
        {'column': 'Band', 'row 1': "Guns 'n' Roses", 'row 2': 'AC/DC', 'row 3': 'Aerosmith'}
    ]
    >>> list(transpose(data[0]))
    [
        {'column': 'fname', 'row 1': 'Axl'},
        {'column': 'lname', 'row 1': 'Rose'},
        {'column': 'Band', 'row 1': "Guns 'n' Roses"}
    ]
    >>> list(transpose("Axl Rose"))
    [{'column': "'Axl Rose'", 'row 1': 'Axl Rose'}]
    >>> pd.DataFrame.from_records(data)
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> df = pd.DataFrame.from_records(data)
    >>> df
        fname  lname            Band
    0     Axl   Rose  Guns 'n' Roses
    1   Angus  Young           AC/DC
    2  Steven  Tyler       Aerosmith
    >>> transpose(df)
    column           row 0  row 1      row 2
    0  fname             Axl  Angus     Steven
    1  lname            Rose  Young      Tyler
    2   Band  Guns 'n' Roses  AC/DC  Aerosmith
    """

    # Add a row number to each row of the data
    count = it.count(1)
    row_num = lambda: next(count)

    # Put the keys into a list
    header = lambda d: list(d.keys())

    # Put the list of values from 1 row into a list of many rows where each
    # value is a single row
    values = lambda d: list(zip(*d.values()))

    # Add the header value to each set of rows
    combine = lambda d: [dict(zip(header(d), row)) for row in values(d)]

    # Return the Table as a list of dict records
    return pipe(
        data
        ,take(limit)
        ,map(lambda row: list(zip(*row.items())))
        ,map(lambda row: dict(zip(["column", f"row {row_num()}"], row)))

        # Merge each record into 1 dict where the keys are the column
        # and row numbers
        ,merge
        ,combine
    )


@transpose.register(pd.DataFrame)
def _(data: pd.DataFrame, limit: int=3) -> pd.DataFrame:
    return pipe(
        data
        .head(limit)

        # Switch columns to rows and rows to columns
        .transpose()

        # Reset the index so that the column containing for column names
        # is named 'index'
        .reset_index()

        # Rename columns using index number as the 'row {col}' part
        ,lambda df: df.rename(columns={
            col: ("column" if col == "index" else f"row {int(col)+1}")
            for col in df.columns
        })
    )


@transpose.register(dict)
def _(data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    for k, v in data.items():
        yield {"column": k, "row 1": v}


@transpose.register(str)
def _(data: str) -> Iterator[Dict[str, Any]]:
    yield {"value": data, "row 1": str(data)}

