# factory/coupon_factory.py


from models.coupon import Coupon, CouponClient
from sql.client import ClientConnector
from strategies.coupon_strategy import PointStrategy, NormalStrategy, DiscountStrategy
import datetime

class CouponFactory:
    def __init__(self, strategy=NormalStrategy()):
        self.strategy = strategy
    
    def process_coupon(self, coupon: Coupon):
        self.strategy.process()
        pass

    def set_strategy(self, strategy):
        self.strategy = strategy

    def create_coupon(self, user_uid, store_uid, item_list, price_list, comment):
        # The provider and consumer of the coupon are the same user initially
        provider_uid = consumer_uid = user_uid

        # Published time is now
        published_time = datetime.datetime.now()

        # Expiration is in 30 days from now
        expiration = published_time + datetime.timedelta(days=30)

        # Create coupon in the database
        with ClientConnector() as client:
            coupon_client = CouponClient(client)
            created_coupon = coupon_client.create(store_uid, provider_uid, consumer_uid, item_list, price_list, published_time, expiration, comment)

        return created_coupon



        
