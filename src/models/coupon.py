# models/coupon.py
from models.table import Table, BaseClient
import datetime
from sql.client import Client

class Coupon(Table):
    def __init__(self, coupon_uid, coupon_type,store_uid ,provider_uid, consumer_uid, item_list=None, price_list=None, published_time=None, 
                 expiration=None, comment=None):
        self.coupon_uid = coupon_uid
        self.coupon_type = coupon_type
        self.store_uid = store_uid
        self.provider_uid = provider_uid
        self.consumer_uid = consumer_uid
        self.item_list = item_list or []
        self.price_list = price_list or []
        self.published_time = published_time
        self.expiration = expiration
        self.comment = comment

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS coupons (
    coupon_uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coupon_type INTEGER,
    store_uid INTEGER REFERENCES stores(store_uid),
    provider_uid INTEGER REFERENCES users(user_uid),
    consumer_uid INTEGER REFERENCES users(user_uid),
    item_list INTEGER[],
    price_list INTEGER[],
    published_time TIMESTAMP,
    expiration TIMESTAMP,
    comment TEXT
);
        """


class CouponClient(BaseClient):
    def __init__(self, client: Client):
        self.db = client

    def create(self, *args):
        query = """
            INSERT INTO coupons (
                coupon_uid, coupon_type, store_uid, provider_uid, consumer_uid, item_list,price_list, published_time, expiration, comment
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)
        if result:
            return Coupon(*result)

    def get(self, coupon_uid):
        query = "SELECT * FROM coupons WHERE coupon_uid = %s;"
        result = self.db.execute(query, (coupon_uid,), fetch_one=True)
        if result:
            return Coupon(*result)
        return None

    def update(self, coupon: Coupon):
        query = """
            UPDATE coupons SET 
                store_uid=%s, provider_uid = %s, consumer_uid = %s, item_list = %s, published_time = %s, 
                expiration = %s, comment = %s
            WHERE coupon_uid = %s;
        """
        self.db.execute(query, (coupon.store_uid, coupon.provider_uid, coupon.consumer_uid, coupon.item_list, 
                                coupon.published_time, coupon.expiration, 
                                coupon.comment, coupon.coupon_uid))


    def update_price(self, coupon_uid, price):
        query = """
            UPDATE coupons SET 
                price_list = %s
            WHERE coupon_uid = %s;
        """
        self.db.execute(query, ([price], coupon_uid))


    def delete(self, coupon_uid):
        query = "DELETE FROM coupons WHERE coupon_uid = %s;"
        self.db.execute(query, (coupon_uid,))
