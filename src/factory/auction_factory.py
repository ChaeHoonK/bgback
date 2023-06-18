# factory/auction_factory.py
from models.auction import Auction
from sql.client import ClientConnector
from models.auction_client import AuctionClient

class AuctionFactory:
    def __init__(self,):
        self.auction_client = None

    def create_auction(self, owner, my_item_list, wish_list):
        """
        Factory method for creating a new auction.
        
        Arguments:
        owner: user_uid of the owner of the auction
        my_item_list: a list of item_uids that the owner is willing to provide
        wish_list: a list of category_uids that the owner is interested in
        
        Returns:
        Auction object
        """
        with ClientConnector() as client:
            self.auction_client = AuctionClient(client)
            auction = Auction(None, owner, my_item_list, wish_list)
            new_auction = self.auction_client.create_auction(auction)
            return new_auction
