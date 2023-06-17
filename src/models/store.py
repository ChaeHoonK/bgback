from models.table import Table

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
