# models/transaction.py
from models.table import Table
import datetime

class Transaction(Table):
    def __init__(self, transaction_uid, timestamp, coupon_uid, client_id, host_id):
        self.transaction_uid = transaction_uid
        self.timestamp = timestamp
        self.coupon_uid = coupon_uid
        self.client_id = client_id
        self.host_id = host_id

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_uid SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    coupon_uid INTEGER,
    client_id INTEGER REFERENCES users(user_uid),
    host_id INTEGER REFERENCES users(user_uid)
);
        """
