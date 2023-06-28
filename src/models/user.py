from models.table import Table, BaseClient
from sql.client import Client

class User(Table):
    def __init__(self, user_uid, email, password, second_password=None, phone_number=None,
                 second_phone_number=None, wallet_id=None, store_uids=None):
        self.user_uid = user_uid
        self.email = email
        self.password = password
        self.second_password = second_password
        self.phone_number = phone_number
        self.second_phone_number = second_phone_number
        self.wallet_id = wallet_id
        self.store_uids = store_uids or []


    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS users (
    user_uid SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    second_password VARCHAR(255),
    phone_number INTEGER,
    second_phone_number INTEGER,
    wallet_id INTEGER,
    store_uids INTEGER[]
);
        """



#models/user_client.py
class UserClient(BaseClient):
    def __init__(self, client:Client, user:User=None):
        self.db = client
        self.user = user

    def create(self, *args):
        try:
            query = """
            INSERT INTO Users (
                email, password, second_password, phone_number, second_phone_number, wallet_id, store_uids
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """
            result = self.db.query(query, args)
            return User(*result)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get(self, userUID):
        try:
            query = "SELECT * FROM Users WHERE userUID = %s;"
            result = self.db.query(query, (userUID,))
            if result:
                return User(*result)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_by_id(self, userUID):
        self.user = self.read(userUID)

    def set_user(self, user: User):
        self.user = user

    def update(self, *args):
        try:
            query = """
            UPDATE Users SET 
                email = %s, password = %s, second_password = %s, phone_number = %s, second_phone_number=%s, wallet_id = %s, store_uids = %s
            WHERE userUID = %s;
            """
            self.db.execute(query, args)
            self.db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, user_uid):
        try:
            query = "DELETE FROM Users WHERE userUID = %s;"
            self.db.execute(query, (user_uid,))
            self.db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
