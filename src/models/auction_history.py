from models.table import Table
import datetime
from sql.client import Client

class AuctionHistory(Table):
    def __init__(self, auction_history_uid, publisher_id, published_time, closed_time, status):
        self.auction_history_uid = auction_history_uid
        self.publisher_id = publisher_id
        self.published_time = published_time
        self.closed_time = closed_time
        self.status = status

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS auction_history (
    auction_history_uid SERIAL PRIMARY KEY,
    publisher_id INTEGER REFERENCES users(user_uid),
    published_time TIMESTAMP,
    closed_time TIMESTAMP,
    status INTEGER
);
        """



class AuctionHistoryClient:
    def __init__(self, client: Client):
        self.db = client

    def create_auction_history(self, *args):
        query = """
            INSERT INTO auction_history (
                auction_history_uid, publisher_id, published_time, closed_time, status
            ) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)
        if result:
            return AuctionHistory(*result)

    def get_auction_history(self, auction_history_uid):
        query = "SELECT * FROM auction_history WHERE auction_history_uid = %s;"
        result = self.db.execute(query, (auction_history_uid,), fetch_one=True)
        if result:
            return AuctionHistory(*result)
        return None

    def update_auction_history(self, auction_history):
        query = """
            UPDATE auction_history SET 
                publisher_id = %s, published_time = %s, closed_time = %s, status = %s
            WHERE auction_history_uid = %s;
        """
        self.db.execute(query, (auction_history.publisher_id, auction_history.published_time,
                                auction_history.closed_time, auction_history.status, auction_history.auction_history_uid))

    def delete_auction_history(self, auction_history_uid):
        query = "DELETE FROM auction_history WHERE auction_history_uid = %s;"
        self.db.execute(query, (auction_history_uid,))