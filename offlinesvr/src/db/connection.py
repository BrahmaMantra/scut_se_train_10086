import os

import clickhouse_connect


# All clickhouse connect use a static local http pool
# so maybe do not need to optimize it
def get_db_client():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 9000))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DB", "default")

    client = clickhouse_connect.get_client(
        host=host, port=port, user=user, password=password, database=database
    )

    return client
