from sql.client import Client
from models.auction_history import AuctionHistory

class AuctionHistoryClient:
    def __init__(self):
        self.db = Client()

    def create_auction_history(self, auction_history):
        query = """
            INSERT INTO auction_history (
                auction_history_uid, publisher_id, published_time, closed_time, status
            ) VALUES (%s, %s, %s, %s, %s);
        """
        self.db.execute(query, (auction_history.auction_history_uid, auction_history.publisher_id,
                                auction_history.published_time, auction_history.closed_time, auction_history.status))

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