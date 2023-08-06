import psycopg2
import pandas as pd

from ovretl.db_utils.fetch_db_credentials import fetch_db_credentials


def select_from_table(entity: str, dbname: str, cluster="dev", after="2015-12-1") -> pd.DataFrame:
    credentials = fetch_db_credentials(cluster=cluster)
    conn = psycopg2.connect(
        host=credentials["host"],
        user=credentials["username"],
        password=credentials["password"],
        dbname=dbname,
        port=credentials["port"],
    )
    sql_query = pd.read_sql_query(
        """
    SELECT * FROM "{}" WHERE created_at > '{}'
    """.format(
            entity, after
        ),
        conn,
    )

    df = pd.DataFrame(sql_query)
    return df
