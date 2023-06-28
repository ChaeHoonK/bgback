#models/item.py

from models.table import Table, BaseClient
from sql.client import Client



class Item(Table):
    def __init__(self, item_uid, name,price,item_type, store_uid, category_l=None, category_m=None, category_s=None):
        self.item_uid = item_uid # Store_id + increment
        self.name = name
        self.price = price
        self.store_uid = store_uid
        self.item_type = item_type # 1: Normal 2: Point 3: Discount
        self.category_l = category_l
        self.category_m = category_m
        self.category_s = category_s

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS items (
    item_uid SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price INTEGER,
    item_type INTEGER,
    store_uid INTEGER REFERENCES stores(store_uid) NOT NULL,
    category_l INTEGER REFERENCES categories_l(category_uid),
    category_m INTEGER REFERENCES categories_m(category_uid),
    category_s INTEGER REFERENCES categories_s(category_uid)
);
        """



class ItemClient(BaseClient):
    def __init__(self, client: Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO items (
                item_uid, name, price, store_uid, category_l, category_m, category_s
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)

        if result:
            return Item(*result)

    def get(self, item_uid):
        query = "SELECT * FROM items WHERE item_uid = %s;"
        result = self.db.execute(query, (item_uid,), fetch_one=True)
        if result:
            return Item(*result)
        return None
    
    def get_by_list(self, item_uids):
        # convert the list to a tuple for sql query
        items_tuple = tuple(item_uids)

        query = f"SELECT * FROM items WHERE item_uid IN %s;"
        result = self.db.execute(query, (items_tuple,))

        if result:
            return [Item(*item) for item in result]
        return []

    def update(self, item):
        query = """
            UPDATE items SET 
                name = %s, category_1 = %s, category_2 = %s, category_3 = %s
            WHERE item_uid = %s;
        """
        self.db.execute(query, (item.name, item.category_1, item.category_2, item.category_3, item.item_uid))

    def delete(self, item_uid):
        query = "DELETE FROM items WHERE item_uid = %s;"
        self.db.execute(query, (item_uid,))