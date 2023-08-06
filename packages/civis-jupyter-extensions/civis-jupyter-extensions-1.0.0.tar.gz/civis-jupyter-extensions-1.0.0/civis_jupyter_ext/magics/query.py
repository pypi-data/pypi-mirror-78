import csv

import pandas as pd
import civis

MAGIC_NAME = 'civisquery'


def magic(line, cell=None):
    """Civis query magic.

    This magic works both as a cell magic (for table previews) and a
    line magic to query a table and return a DataFrame.

    You can pass either a database name or an ID in the below. If your database
    name contains a space and you are using the line magic, you must quote
    delimit the database.

    If your version of Python supports it, F-string interpolation will work on
    the line in both the line and cell magics but not the cell of a cell magic.
    This isn't currently supported in IPython.

    Examples
    --------

    Use the cell magic

    >>> %%civisquery DATABASE
    ... SELECT * FROM schema.table;

    Use the line magic

    >>> %civisquery DATABASE QUERY

    Use f-strings with the line magic

    >>> %civisquery {DATABASE_ID} {SQL_STATEMENT}

    Use f-strings with the cell magic

    >>> %%civisquery {DATABASE}
    SELECT * FROM schema.table;

    Query a database name with spaces

    >>> %civisquery "My Database" {SQL_STATEMENT}

    Cell magic for a database with a space

    >>> %%civisquery My Database
    SELECT * FROM schema.table
    """

    client = civis.APIClient()

    if cell is None:
        reader = csv.reader(
            [line],
            delimiter=" ",
            quotechar='"',
            doublequote=True,
            skipinitialspace=True)
        parsed_line = next(reader)

        database, lines = parsed_line[0], parsed_line[1:]

        sql = " ".join(lines)
        try:
            # if it's an integer, read_civis_sql will let it pass through
            # but if you pass an integer to the magic it gets coerced to
            # a string. it will try to look up an integer string as a
            # database name and will fail to find that name
            database = int(database.strip())
        except ValueError:
            database = database.strip()

        df = civis.io.read_civis_sql(
            sql.strip(), database, use_pandas=True, client=client)
        if len(df) == 0:
            df = None
    else:
        database = line.strip()

        try:  # support database IDs like line magic
            database = int(database)
        except ValueError:
            pass

        sql = cell

        fut = civis.io.query_civis(
            sql, database, client=client, preview_rows=100)
        res = fut.result()
        if len(res['result_rows']) > 0:
            df = pd.DataFrame.from_records(
                res['result_rows'], columns=res['result_columns'])
        else:
            df = None

    return df
