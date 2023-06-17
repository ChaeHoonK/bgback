# models/auction.py
from models.table import Table

class Auction(Table):
    def __init__(self, auction_uid, owner, my_item_list=None, wish_list=None):
        self.auction_uid = auction_uid
        self.owner = owner
        self.my_item_list = my_item_list or []
        self.wish_list = wish_list or []

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS auctions (
    auction_uid SERIAL PRIMARY KEY,
    owner INTEGER REFERENCES users(user_uid),
    my_item_list INTEGER[],
    wish_list INTEGER[]
);
        """
