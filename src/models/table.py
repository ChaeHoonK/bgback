from sql.client import Client, ClientConnector


class Table:
    @classmethod
    def _ensure_table_sql(cls) -> str:
        raise NotImplementedError

    @classmethod
    def ensure_table(cls):
        print('initializing ' + str(cls.__name__))
        with ClientConnector() as client:
            client.execute(cls._ensure_table_sql())
