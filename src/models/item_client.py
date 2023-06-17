from sql.client import Client
from models.item import Item

class ItemsClient:
    def __init__(self):
        self.db = Client()

    def create_item(self, name, category_1, category_2, category_3):
        query = """
            INSERT INTO items (
                item_uid, name, category_1, category_2, category_3
            ) VALUES (DEFAULT, %s, %s, %s, %s);
        """
        self.db.execute(query, (name, category_1, category_2, category_3))

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