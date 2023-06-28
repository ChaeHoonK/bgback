from models.table import Table, BaseClient
from sql.client import Client

class Store(Table):
    def __init__(self, store_uid, phone_number, name, latitude, longitude,
                 address, category_l=None, category_m=None, category_s=None, menu_items=None, menu_prices=None, urls=None, employees=None):
        self.store_uid = store_uid
        self.phone_number = phone_number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.category_l = category_l
        self.category_m = category_m
        self.category_s = category_s
        self.menu_items = menu_items or []
        self.menu_prices = menu_prices or []
        self.urls = urls or []
        self.employees = employees or []

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
    category_l INT REFERENCES categories_l(category_uid),
    category_m INT REFERENCES categories_m(category_uid),
    category_s INT REFERENCES categories_s(category_uid),
    menu_items INTEGER[], -- Array of item UIDs,
    menu_prices INTEGER[],
    urls TEXT[],
    employees INTEGER[] -- Array of user_UIDs
);
        """
    

class StoreClient(BaseClient):
    def __init__(self, client:Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO stores (
                store_uid, phone_number, name, latitude, longitude, address,category_l, category_m, category_s, menu_items, menu_prices, urls, employees
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)
        if result:
            return Store(*result)

    def get(self, store_uid):
        query = "SELECT * FROM stores WHERE store_uid = %s;"
        result = self.db.execute(query, (store_uid,), fetch_one=True)
        if result:
            return Store(*result)
        return None

    def update(self, store):
        query = """
            UPDATE stores SET 
                phone_number = %s, name = %s, latitude = %s, longitude = %s, address = %s, 
                menu_items = %s, urls = %s
            WHERE store_uid = %s;
        """
        self.db.execute(query, (store.phone_number, store.name, store.latitude, store.longitude, 
                                store.address, store.menu_items, store.urls, store.store_uid))

    def delete(self, store_uid):
        query = "DELETE FROM stores WHERE store_uid = %s;"
        self.db.execute(query, (store_uid,))

