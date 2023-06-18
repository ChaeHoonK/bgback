# models/transaction.py
from models.table import Table
from sql.client import Client
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



class TransactionClient:
    def __init__(self, client: Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO transactions (
                transaction_uid, timestamp, coupon_uid, client_id, host_id
            ) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)

    def get(self, transaction_uid):
        query = "SELECT * FROM transactions WHERE transaction_uid = %s;"
        result = self.db.execute(query, (transaction_uid,), fetch_one=True)
        if result:
            return Transaction(*result)
        return None

    def update(self, transaction: Transaction):
        query = """
            UPDATE transactions SET 
                timestamp = %s, coupon_uid = %s, client_id = %s, host_id = %s
            WHERE transaction_uid = %s;
        """
        self.db.execute(query, (transaction.timestamp, transaction.coupon_uid, 
                                transaction.client_id, transaction.host_id, 
                                transaction.transaction_uid))

    def delete(self, transaction_uid):
        query = "DELETE FROM transactions WHERE transaction_uid = %s;"
        self.db.execute(query, (transaction_uid,))
