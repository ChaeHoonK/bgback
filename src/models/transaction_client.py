# models/transaction_client.py
from sql.client import Client as Client
from models.transaction import Transaction

class TransactionClient:
    def __init__(self):
        self.db = Client()

    def create_transaction(self, transaction: Transaction):
        query = """
            INSERT INTO transactions (
                transaction_uid, timestamp, coupon_uid, client_id, host_id
            ) VALUES (%s, %s, %s, %s, %s);
        """
        self.db.execute(query, (transaction.transaction_uid, transaction.timestamp, 
                                transaction.coupon_uid, transaction.client_id, 
                                transaction.host_id))

    def get_transaction(self, transaction_uid):
        query = "SELECT * FROM transactions WHERE transaction_uid = %s;"
        result = self.db.execute(query, (transaction_uid,), fetch_one=True)
        if result:
            return Transaction(*result)
        return None

    def update_transaction(self, transaction: Transaction):
        query = """
            UPDATE transactions SET 
                timestamp = %s, coupon_uid = %s, client_id = %s, host_id = %s
            WHERE transaction_uid = %s;
        """
        self.db.execute(query, (transaction.timestamp, transaction.coupon_uid, 
                                transaction.client_id, transaction.host_id, 
                                transaction.transaction_uid))

    def delete_transaction(self, transaction_uid):
        query = "DELETE FROM transactions WHERE transaction_uid = %s;"
        self.db.execute(query, (transaction_uid,))
