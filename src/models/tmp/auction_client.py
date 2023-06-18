# models/auction_client.py
from sql.client import Client
from models.auction import Auction

class AuctionClient:
    def __init__(self,client: Client):
        self.db = client

    def create_auction(self, auction: Auction):
        query = """
            INSERT INTO auctions (
                auction_uid, owner, item_list, price_list, wish_list
            ) VALUES (DEFAULT, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, (auction.owner, auction.item_list, auction.price_list, 
                                         auction.wish_list), fetch_one=True)
        if result:
            return Auction(*result)

    def get_auction(self, auction_uid):
        query = "SELECT * FROM auctions WHERE auction_uid = %s;"
        result = self.db.query(query, (auction_uid,), fetch_one=True)
        if result:
            return Auction(*result)
        return None

    def update_auction(self, auction: Auction):
        query = """
            UPDATE auctions SET 
                owner = %s, item_list = %s, price_list = %s ,wish_list = %s
            WHERE auction_uid = %s;
        """
        self.db.execute(query, (auction.owner, auction.item_list, auction.price_list, 
                                auction.wish_list, auction.auction_uid))

    def delete_auction(self, auction_uid):
        query = "DELETE FROM auctions WHERE auction_uid = %s;"
        self.db.execute(query, (auction_uid,))
