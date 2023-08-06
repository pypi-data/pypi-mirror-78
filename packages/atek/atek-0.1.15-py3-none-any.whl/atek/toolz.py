#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from fnmatch import fnmatch
from tabulate import tabulate
from cytoolz.curried import pipe, curry, take, identity, map
from textwrap import fill
from typing import *
import atek
from pathlib import Path

__all__ = ["is_df", "filter_col", "valid_path"]

def is_df(obj: Any, param_name: str="dataframe") -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj

    raise ValueError(f"arg '{param_name}' must be a pandas.DataFrame")

Record = Dict[str, Any]
Table = Iterable[Record]
TableOrDF = Union[pd.DataFrame, Table]

def to_records(data: TableOrDF) -> Table:
    return (
        data.to_dict("records") if isinstance(data, pd.DataFrame) else 
        data if isinstance(data, list) else 
        [row for row in data]
    )
        

@curry
def filter_col(patterns: Union[str, List[str]],
    data: TableOrDF) -> TableOrDF:
    """Filters the columns of a dataframe using list
    of fnmatch patterns."""

    patterns = [patterns] if isinstance(patterns, str) else patterns
    def get_cols(cols, pats):
        return [
            col
            for col in cols
            for pat in pats
            if fnmatch(col.lower(), pat.lower())
        ]

    if isinstance(data, pd.DataFrame):
        return data.filter(get_cols(data.columns, patterns))

    if isinstance(data, Iterable):
        return pipe(
            data
            ,map(lambda d: {
                k: v
                for k, v in d.items()
                if k in get_cols([k for k in d], patterns)
            })
        )

def valid_path(path: Union[str, Path]) -> Path:
    """Returns a valid pathlib.Path object or provides smart error message
    indicating which parts are valid (exist) and which parts do not exist."""
    _path = Path(path).expanduser()
    # If expanded path or directory exists then return the expanded path
    if _path.exists():
        return _path

    # If expanded path doesn't exist, return a helpful error message by
    # calculating the good part (exists) of the path and the bad part of 
    # path
    temp = _path.parent
    while True:
        if temp.exists():
            bad_part = _path.relative_to(temp)
            raise ValueError(
                f"{_path} does not exist."
                f"Good part = {temp}, "
                f"Bad part = {bad_part}"
            )
        temp = temp.parent

    
if __name__ == "__main__":
    pipe(
        atek.query_atek02_main("select * from orders limit 3")
        ,pd.DataFrame.from_records
        ,to_records
        ,filter_col("*del*date*")
        ,list
        ,atek.transpose
        ,atek.show
    )

    print(f"SUCCESS: {valid_path('~/OneDrive - AppraisalTek/Reports')=}")
    try:
        print(valid_path("~/OneDrive - AppraisalTek/some folder"))
    except ValueError as err:
        print(f"FAILURE: {err=}")
