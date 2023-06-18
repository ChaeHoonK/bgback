from models.table import Table
from sql.client import Client

class Item(Table):
    def __init__(self, item_uid, name, category_1=None, category_2=None, category_3=None):
        self.item_uid = item_uid
        self.name = name
        self.category_1 = category_1
        self.category_2 = category_2
        self.category_3 = category_3

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS items (
    item_uid SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category_1 INTEGER,
    category_2 INTEGER,
    category_3 INTEGER
);
        """



class ItemsClient:
    def __init__(self, client: Client):
        self.db = client

    def create_item(self, *args):
        query = """
            INSERT INTO items (
                item_uid, name, category_1, category_2, category_3
            ) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)

        if result:
            return Item(*result)

    def get_item(self, item_uid):
        query = "SELECT * FROM items WHERE item_uid = %s;"
        result = self.db.execute(query, (item_uid,), fetch_one=True)
        if result:
            return Item(*result)
        return None

    def update_item(self, item):
        query = """
            UPDATE items SET 
                name = %s, category_1 = %s, category_2 = %s, category_3 = %s
            WHERE item_uid = %s;
        """
        self.db.execute(query, (item.name, item.category_1, item.category_2, item.category_3, item.item_uid))

    def delete_item(self, item_uid):
        query = "DELETE FROM items WHERE item_uid = %s;"
        self.db.execute(query, (item_uid,))