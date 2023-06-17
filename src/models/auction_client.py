# models/auction_client.py
from sql.client import Client
from models.auction import Auction

class AuctionClient:
    def __init__(self):
        self.db = Client()

    def create_auction(self, auction: Auction):
        query = """
            INSERT INTO auctions (
                auction_uid, owner, my_item_list, wish_list
            ) VALUES (%s, %s, %s, %s);
        """
        self.db.execute(query, (auction.auction_uid, auction.owner, 
                                auction.my_item_list, auction.wish_list))

    def get_auction(self, auction_uid):
        query = "SELECT * FROM auctions WHERE auction_uid = %s;"
        result = self.db.execute(query, (auction_uid,), fetch_one=True)
        if result:
            return Auction(*result)
        return None

    def update_auction(self, auction: Auction):
        query = """
            UPDATE auctions SET 
                owner = %s, my_item_list = %s, wish_list = %s
            WHERE auction_uid = %s;
        """
        self.db.execute(query, (auction.owner, auction.my_item_list, 
                                auction.wish_list, auction.auction_uid))

    def delete_auction(self, auction_uid):
        query = "DELETE FROM auctions WHERE auction_uid = %s;"
        self.db.execute(query, (auction_uid,))
