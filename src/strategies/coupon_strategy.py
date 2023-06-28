# strategies/coupon_strategy.py
from sql.client import ClientConnector
from models.transaction import Transaction, TransactionClient
from models.coupon import Coupon, CouponClient

class Strategy:
    def __init__(self):
        pass

    def process(self, amount = None):
        pass

    @classmethod
    def generate_strategy(cls, coupon_type:int):
        d = {1:NormalStrategy(), 2: PointStrategy(), 3: DiscountStrategy()}

        result = d[coupon_type]

        if result is None:
            raise ValueError(f"Input coupon_type value: '{coupon_type}' does not exist.")

        return d[type]

class NormalStrategy(Strategy):

    def process(self, coupon:Coupon , amount = None):
        with ClientConnector() as client:
            coupon_client = CouponClient(client)
            coupon_client.delete(coupon.coupon_uid)


class PointStrategy(Strategy):

    def process(self, coupon:Coupon, amount = None):
        with ClientConnector() as client:
            coupon_client = CouponClient(client)

            # Calculate the new price after discount
            new_price = sum(coupon.price_list) - amount

            if new_price > 0:
                # Update the item price in the coupon
                coupon_client.update_price(coupon.coupon_uid, new_price)
            else:
                # Delete the coupon if the new price is less than or equal to 0
                coupon_client.delete(coupon.coupon_uid)


class DiscountStrategy(Strategy):

   def process(self, coupon: Coupon, amount = None):
        with ClientConnector() as client:
            coupon_client = CouponClient(client)
            coupon_client.delete(coupon.coupon_uid)