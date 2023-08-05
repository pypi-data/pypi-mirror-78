"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pandas as pd
import pymysql
from pymysql.cursors import Cursor, SSDictCursor
from pymysql.connections import Connection
from pathlib import Path
from typing import *
from configparser import ConfigParser
from contextlib import contextmanager
import os
import requests
from cytoolz.curried import pipe, partial, curry, get_in, take, map, merge
from textwrap import fill
from tabulate import tabulate
import itertools as it

__all__ = "config query_atek02_main query_acad_domo transpose show".split()


def parse_config(config_path: str):
    """Reads a config file using configparser.ConfigParser from the standard library
    and converts any values with address in the key name to a ip address and port 
    combination."""
    config = ConfigParser()
    path = Path(config_path).expanduser()
    config.read(path)
    settings = {
        section: {
            key: (
                tuple([
                    value.split()[0], 
                    int(value.split()[1])
                ]) if "address" in key else 
                value
            )
            for key, value in config[section].items()
        }
        for section in config.sections()
    }
    return settings


def config(env_var: str, *keys: str):
    """Returns the values in a config file as a dict or nested dict using an 
    environment value ('env_var') which refers to a path. 
    # 'path/to/some/config/file'
    [section 1]
    param1 = value1
    param2 = value2

    [section 2]
    parama = valuea
    paramb = valueb

    SOME_VAR='path/to/some/config/file'
    >>> config("SOME_VAR")
    {"section 1": {"param1": "value1", "param2": "value2"},
    "section 2": {"parama": "valuea", "paramb": "valueb"}}

    >>> config("SOME_VAR", "section 1")
    {"param1": "value1", "param2": "value2"}

    >>> config("SOME_VAR", "section 1", "param2")
    "value2"

    """
    # Get the enironment variable with a default of '' if it doesn't exist
    env_value = os.getenv(env_var, "")
    assert env_value != "", "f{env_var=} doesn't exist or returned ''"

    # Return the dict or potentially nested dict from parse_config
    settings = parse_config(env_value)

    # Return the value using nested keys
    return get_in([*keys], settings)


@contextmanager
def connect_atek02_main() -> Connection:
    """Creates a ssh tunnel and returns a connection options to atek02_main."""

    # Establish the ssh tunnel
    with SSHTunnelForwarder(**config("ATEK02_MAIN", "public_html")) as tunnel:

        # Create a connection to the database and a lazy cursor
        conn = pymysql.connect(
            **config("ATEK02_MAIN", "atek02_main"),
            port=tunnel.local_bind_port,
            cursorclass=SSDictCursor
        )

        yield conn

        conn.close()


Record = Dict[str,Any]
Table = Iterable[Record]

def query_atek02_main(sql: str) -> Table:
    """Returns a generator of dict objects as records."""

    with connect_atek02_main() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall_unbuffered()
        for row in rows:
            yield row


def connect_acad_domo():
    """Returns an authorization header used in working with a domo
    instance api."""

    # Get client_id and token from config file and obtain an auth token
    domo = config("ACADEMY_DOMO", "acad_domo")
    auth = requests.auth.HTTPBasicAuth(domo["client_id"], domo["secret"])
    response = requests.get(domo["auth_url"], auth=auth)
    token = response.json()["access_token"]

    # Create and return the authorization header
    header = {"Authorization": f"bearer {token}"}
    return header


def datasets_acad_domo(name_or_id: Optional[str]=None,
    env_var: str="ACADEMY_DOMO") -> Table:
    """Retrieves a list of datasets from the domo instance for which the
    token has access."""

    header = connect_acad_domo()
    limit = 50
    offset = 0
    base_url = config(env_var, "acad_domo", "base_url")

    # Cycle through the list in chunks of 'limit'
    while True:
        url = f"{base_url}?offset={offset}&limit={limit}"
        chunk = requests.get(url, headers=header).json()
        if not chunk: break
        for row in chunk:
            # If name or id provided then only yield a row if it matches
            name = row["name"]
            id = row["id"]

            if name_or_id: 
                if name_or_id == name or name_or_id == id:
                    yield row
                else:
                    pass

            # If name and id are not provided yield all rows
            else:
                yield row
        offset += limit


@curry
def query_acad_domo(name_or_id: str, sql: str=""):

    # Create the header
    header = connect_acad_domo()
    header["Accept"] = "application/json"
    sql = "select * from table" if sql == "" else sql
    query = {"sql": sql}
    base_url = config("ACADEMY_DOMO", "acad_domo", "base_url")

    # Get thet table id
    table = list(datasets_acad_domo(name_or_id))
    assert len(table) > 0, "Returned dataset is empty... check the provided " \
        "'name_or_id' parameter."

    id = table[0]["id"]
    url = f"{base_url}/query/execute/{id}?includeHeaders=true"

    # Get the table in json formaatt
    response = requests.post(url, headers=header, json=query).json()
    
    # Assembe the table as a list of dict objects
    columns = response["columns"]
    rows = response["rows"]
    data = [
        dict(zip(columns, row))
        for row in rows
    ]

    # lazily return the data
    for row in data:
        yield row


DF_Table_Dict = Union[pd.DataFrame, Table, Record]

def transpose_table(data: Table, limit: int=3) -> Table:
    """Transposes a table (list of dicts) such that columns are
    rows and rows are columns.
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


def transpose_dataframe(data: pd.DataFrame, limit: int=3):
    """Transpose a pandas DataFrame
    >>> df = pandas.DataFrame({
        "first_name": ["Santa", "Kris"], 
        "last_name": ["Claus", "Kringle"]
    })
    >>> df
      first_name last_name
    0      Santa     Claus
    1       Kris   Kringle
    >>> transpose_dataframe(df)
       column  row 0    row 1
    0  first_name  Santa     Kris
    1  last_name  Claus  Kringle
    """
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
            col: ("column" if col == "index" else f"row {col}")
            for col in df.columns
        })
    )


def transpose_record(data: Record) -> Table:
    """Convert a dict into a list of dicts where each dict represents a 
    key value pair.
    >>>transpose_record({"first_name", "Santa", "last_name": "Claus"})
    [{"column": "first_name", "row 1": "Santa"},
     {"column": "last_name", "row 1": "Claus"}]
    """
    return [
        {"column": k, "row 1": v}
        for k, v in data.items()
     ]


def is_df_table_dict(data: Any) -> DF_Table_Dict:
    """Check to see if 'data' is a dict, iterable of dicts, or pandas 
    DataFrame. If it is return data otherwise return an AssertError."""

    msg = "data must be a dict, pandas DataFrame or iterable of dicts"
    assert data is not None, msg 
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, dict):
        return data
    elif isinstance(data, Iterable):
        return data
    else:
        raise AssertError(msg)


@curry
def transpose(data: DF_Table_Dict, limit: int=3) -> DF_Table_Dict:
    """Transpose a dict, iterable of dicts, or pandas DataFrame."""
    return pipe(
        data
        ,is_df_table_dict
        ,lambda x: (
            transpose_record(data) if isinstance(x, dict) else
            transpose_dataframe(data, limit) if isinstance(x, pd.DataFrame) else
            transpose_table(data, limit)
        )
    )


@curry
def show(data: DF_Table_Dict, column_width: int=25, 
         print_out: bool = True, limit: int=100, caption: Optional[str]=None, 
    **kwds) -> str:

    # Check data is correct type
    assert data is not None, "data must be an iterable of dict objects"
    if data is None:
        raise ValueError(
            "data must be an iterable of dict objects or a pandas DataFrame")

    else:
        table = (
            [{"value": data}] if isinstance(data, str) else 
            data.head(limit).to_dict("records") if isinstance(data,  pd.DataFrame) else 
            [
                {"key": k, "value": v}
                for k, v in data.items()
             ] if isinstance(data, dict) else
            list(take(limit, data))
        )

    # Function to wrap the row value
    def wrap_value(value):
        return (
            '' if value is None else fill(str(value), column_width)
        )

    # Function to wrap the column name
    def wrap_key(value):
        if isinstance(value, str):
            return fill(str(value), column_width)
        else:
            raise TypeError("Key must be a str type")

    # Verify that each row is a dict object
    def is_dict(row, row_number=None):
        if isinstance(row, dict):
            return row
        else:
            raise TypeError(f"row at {row_number=} is not a dict\n{row=}")
        

    wrapped = [
        {
            wrap_key(k): wrap_value(v)
            for k, v in is_dict(row, row_number).items()
        }
        for row_number, row in enumerate(table, start=1)
    ]

    defaults = {
        "headers": "keys", 
        "tablefmt": "fancy_grid"
    }

    args = {**defaults, **kwds}

    table = tabulate(wrapped, **args)

    if print_out:
        if caption: print(f"\n{caption}")
        print(table)

    return table


if __name__ == "__main__":

    sql = """
    select TrackingNumber, LoanNumber, OrderDate
    from table
    limit 3
    """

    domo = pipe(
        query_acad_domo(
            "Prod - Appraisal - Mercury Appraisal No PDP",
            "select TrackingNumber, LoanNumber, OrderDate from table limit 3"
        )
        ,list
    )

    pipe(
        domo
        ,show(caption="acad_domo")
    )

    pipe(
        domo
        ,transpose
        ,show(caption="acad_domo transposed")
    )

    pipe(
        domo
        ,pd.DataFrame.from_records
        ,transpose
        ,show(caption="acad_domo dataframe transposed")
    )

    sql =  """
    select
    database() as current_database
    ,current_user() as login_user
    ,version() as version
    ,now() as connected
    """

    show(query_atek02_main(sql), caption="atek02_main")
    show(transpose(query_atek02_main(sql)), caption="transposed atek02_main")
