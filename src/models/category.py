from models.table import Table

class Category(Table):
    def __init__(self, category_uid, name):
        self.category_uid = category_uid
        self.name = name

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS categories (
    category_uid SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
        """
