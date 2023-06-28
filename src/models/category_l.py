from models.table import Table, BaseClient
from sql.client import Client

class Category(Table):
    def __init__(self, category_uid, name):
        self.category_uid = category_uid
        self.name = name

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS categories_l (
    category_uid SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
        """




class CategoryClient(BaseClient):
    def __init__(self,client: Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO categories_l (
                DEFAULT, name
            ) VALUES (%s) RETURNING *;
        """
        result = self.db.query(query, args)

        if result:
            return Category(*result)

    def get(self, category_uid):
        query = "SELECT * FROM categories_l WHERE category_uid = %s;"
        result = self.db.execute(query, (category_uid,), fetch_one=True)
        if result:
            return Category(*result)
        return None

    def update(self, category: Category):
        query = """
            UPDATE categories_l SET 
                name = %s
            WHERE category_uid = %s;
        """
        self.db.execute(query, (category.name, category.category_uid))

    def delete(self, category_uid):
        query = "DELETE FROM categories_l WHERE category_uid = %s;"
        self.db.execute(query, (category_uid,))