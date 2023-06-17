# models/__init__.py
from models.user import User
from models.wallet import Wallet
from models.store import Store
from models.item import Item
from models.category import Category
from models.auction_history import AuctionHistory
from models.transaction import Transaction
from models.coupon import Coupon
from models.request import Request
from models.auction import Auction
from time import sleep

def init_all():
    Category.ensure_table()
    User.ensure_table()
    Wallet.ensure_table()
    Store.ensure_table()
    Item.ensure_table()
    AuctionHistory.ensure_table()
    Transaction.ensure_table()
    Coupon.ensure_table()
    Request.ensure_table()
    Auction.ensure_table()
    
