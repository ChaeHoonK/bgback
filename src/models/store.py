from models.table import Table
from sql.client import Client

class Store(Table):
    def __init__(self, store_uid, phone_number, name, latitude, longitude,
                 address, menu_items=None, urls=None):
        self.store_uid = store_uid
        self.phone_number = phone_number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.menu_items = menu_items or []
        self.urls = urls or []

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS stores (
    store_uid SERIAL PRIMARY KEY,
    phone_number INTEGER,
    name VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    address VARCHAR(255),
    menu_items INTEGER[], -- Array of item UIDs
    urls TEXT[]
);
        """
    

class StoreClient:
    def __init__(self, client:Client):
        self.db = client

    def create_store(self, *args):
        query = """
            INSERT INTO stores (
                store_uid, phone_number, name, latitude, longitude, address, menu_items, urls
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)
        if result:
            return Store(*result)

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

