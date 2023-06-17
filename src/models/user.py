from models.table import Table

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
