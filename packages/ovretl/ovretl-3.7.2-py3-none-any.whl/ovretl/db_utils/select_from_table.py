import psycopg2
import pandas as pd

from ovretl.db_utils.fetch_db_credentials import fetch_db_credentials


def select_from_table(entity: str, cluster="dev", after="2015-12-1", dbname=None) -> pd.DataFrame:
    """
    dbname is necessary to fetch Rates DB in dev & prod cluster
    :param entity:
    :param cluster:
    :param after:
    :param dbname:
    :return:
    """
    credentials = fetch_db_credentials(cluster=cluster)
    conn = psycopg2.connect(
        host=credentials["host"],
        user=credentials["username"],
        password=credentials["password"],
        dbname=dbname or credentials["dbname"],
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
