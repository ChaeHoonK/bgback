from sql.client import Client


class Table:
    @classmethod
    def _ensure_table_sql(cls) -> str:
        raise NotImplementedError

    @classmethod
    def ensure_table(cls):
        print('initializing ' + str(cls.__name__))
        client = Client()
        client.cursor.execute(cls._ensure_table_sql())
        client.connection.commit()
        client.connection.close()
        client.cursor.close()