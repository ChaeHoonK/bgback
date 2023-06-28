# models/auction.py
from models.table import Table, BaseClient
from sql.client import Client

class Auction(Table):
    def __init__(self, auction_uid, publisher, published_time, item_list=None, price_list=None, wish_list=None):
        self.auction_uid = auction_uid
        self.publisher = publisher
        self.published_time = published_time
        self.item_list = item_list or []
        self.price_list = price_list or []
        self.wish_list = wish_list or []

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS auctions (
    auction_uid SERIAL PRIMARY KEY,
    publisher INTEGER REFERENCES users(user_uid),
    published_time TIMESTAMP,
    item_list INTEGER[],
    price_list INTEGER[],
    wish_list INTEGER[]
);
        """



class AuctionClient (BaseClient):
    def __init__(self,client: Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO auctions (
                auction_uid, publisher, published_time, item_list, price_list, wish_list
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args, fetch_one=True)
        if result:
            return Auction(*result)

    def get(self, auction_uid):
        query = "SELECT * FROM auctions WHERE auction_uid = %s;"
        result = self.db.query(query, (auction_uid,), fetch_one=True)
        if result:
            return Auction(*result)
        return None

    def update(self, auction: Auction):
        query = """
            UPDATE auctions SET 
                owner = %s, item_list = %s, price_list = %s ,wish_list = %s
            WHERE auction_uid = %s;
        """
        self.db.execute(query, (auction.owner, auction.item_list, auction.price_list, 
                                auction.wish_list, auction.auction_uid))

    def delete(self, auction_uid):
        query = "DELETE FROM auctions WHERE auction_uid = %s;"
        self.db.execute(query, (auction_uid,))
