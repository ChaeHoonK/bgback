from sql.client import Client
from models.category import Category

class CategoryClient:
    def __init__(self):
        self.db = Client()

    def create_category(self, name):
        query = """
            INSERT INTO categories (
                DEFAULT, name
            ) VALUES (%s);
        """
        self.db.execute(query, (name))

    def get_category(self, category_uid):
        query = "SELECT * FROM categories WHERE category_uid = %s;"
        result = self.db.execute(query, (category_uid,), fetch_one=True)
        if result:
            return Category(*result)
        return None

    def update_category(self, category):
        query = """
            UPDATE categories SET 
                name = %s
            WHERE category_uid = %s;
        """
        self.db.execute(query, (category.name, category.category_uid))

    def delete_category(self, category_uid):
        query = "DELETE FROM categories WHERE category_uid = %s;"
        self.db.execute(query, (category_uid,))