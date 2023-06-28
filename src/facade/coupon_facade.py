# facade/coupon_facade.py

from models.request import Request
from models.coupon import Coupon, CouponClient
from models.item import Item, ItemClient
from models.transaction import Transaction, TransactionClient

from strategies.coupon_strategy import Strategy
from sql.client import ClientConnector

import datetime


class CouponFacade:
    def __init__(self):
        self.strategy:Strategy = None

    def _set_strategy(self, strategy):
        self.strategy = strategy

    def create_coupon(self, request: Request, sender_comment=None, receiver_comment=None,):
        sender_coupon = self._create_coupon(request.sender_user_uid, request.sender_store_uid,
                                                   request.sender_item_list, 
                                                   request.sender_price_list, sender_comment)

        receiver_coupon = self._create_coupon(request.receiver_user_uid, request.receiver_store_uid,
                                                     request.receiver_item_list, 
                                                     request.receiver_price_list, receiver_comment)

        return [sender_coupon, receiver_coupon]


    def process_coupon(self, coupon: Coupon, amount) -> Transaction:
        self._set_strategy(Strategy.generate_strategy(coupon.coupon_type))
        if self.strategy is not None:
            self.strategy.process(coupon, amount)

        # Create a transaction after processing the coupon
        with ClientConnector() as client:
            transaction_client = TransactionClient(client)
            transaction = transaction_client.create(coupon.coupon_uid, datetime.datetime.now(), coupon.consumer_uid, amount)

        return transaction
        

    def _create_coupon(self, store_uid, provider_uid, consumer_uid, item_list, price_list, comment):
        # Published time is now

        published_time = datetime.datetime.now()

        # Expiration is in 30 days from now
        expiration = published_time + datetime.timedelta(days=30)

        coupons = []
        # Create coupon in the database
        with ClientConnector() as client:
            coupon_client = CouponClient(client)
            item_client = ItemClient(client)

            items = item_client.get_by_list(item_list)

            grouped_items = self._group_items_by_type(items, price_list)

            for coupon_type, (item_uids, prices) in grouped_items.items():
                coupon = coupon_client.create(coupon_type, store_uid, provider_uid, consumer_uid, item_uids, prices, published_time, expiration, comment)
                coupons.append(coupon)

        return coupons
    
    def _group_items_by_type(self, items:list[Item], prices:list[int]):
        # Make sure items and prices have the same length
        assert len(items) == len(prices)

        grouped_items:dict[int, tuple[(list[int], list[int])]] = {}
        for item, price in zip(items, prices):
            # If the item type is not already in the dictionary, create a new entry
            if item.item_type not in grouped_items:
                grouped_items[item.item_type] = ([], [])
            
            # Add the item uid and price to the corresponding lists in the dictionary
            grouped_items[item.item_type][0].append(item.item_uid)
            grouped_items[item.item_type][1].append(price)

        return grouped_items