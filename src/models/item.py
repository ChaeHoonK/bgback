from models.table import Table

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
