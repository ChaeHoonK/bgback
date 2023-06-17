from sql.client import Client
from models.store import Store

class StoreClient:
    def __init__(self):
        self.db = Client()

    def create_store(self, store):
        query = """
            INSERT INTO stores (
                store_uid, phone_number, name, latitude, longitude, address, menu_items, urls
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.db.execute(query, (store.store_uid, store.phone_number, store.name, store.latitude, 
                                store.longitude, store.address, store.menu_items, store.urls))

    def get_store(self, store_uid):
        query = "SELECT * FROM stores WHERE store_uid = %s;"
        result = self.db.execute(query, (store_uid,), fetch_one=True)
        if result:
            return Store(*result)
        return None

    def update_store(self, store):
        query = """
            UPDATE stores SET 
                phone_number = %s, name = %s, latitude = %s, longitude = %s, address = %s, 
                menu_items = %s, urls = %s
            WHERE store_uid = %s;
        """
        self.db.execute(query, (store.phone_number, store.name, store.latitude, store.longitude, 
                                store.address, store.menu_items, store.urls, store.store_uid))

    def delete_store(self, store_uid):
        query = "DELETE FROM stores WHERE store_uid = %s;"
        self.db.execute(query, (store_uid,))
