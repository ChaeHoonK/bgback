from models.table import Table
import datetime

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
