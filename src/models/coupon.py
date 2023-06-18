# models/coupon.py
from models.table import Table
import datetime
from sql.client import Client

class Coupon(Table):
    def __init__(self, coupon_uid, user_1_uid, user_2_uid, item_list=None, published_time=None, 
                 expiration=None, comment=None):
        self.coupon_uid = coupon_uid
        self.user_1_uid = user_1_uid
        self.user_2_uid = user_2_uid
        self.item_list = item_list or []
        self.published_time = published_time
        self.expiration = expiration
        self.comment = comment

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS coupons (
    coupon_uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_1_uid INTEGER REFERENCES users(user_uid),
    user_2_uid INTEGER REFERENCES users(user_uid),
    item_list INTEGER[],
    published_time TIMESTAMP,
    expiration TIMESTAMP,
    comment TEXT
);
        """


class CouponClient:
    def __init__(self, client: Client):
        self.db = client

    def create_coupon(self, *args):
        query = """
            INSERT INTO coupons (
                coupon_uid, user_1_uid, user_2_uid, item_list, published_time, expiration, comment
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, args)
        if result:
            return Coupon(*result)

    def get_coupon(self, coupon_uid):
        query = "SELECT * FROM coupons WHERE coupon_uid = %s;"
        result = self.db.execute(query, (coupon_uid,), fetch_one=True)
        if result:
            return Coupon(*result)
        return None

    def update_coupon(self, coupon: Coupon):
        query = """
            UPDATE coupons SET 
                user_1_uid = %s, user_2_uid = %s, item_list = %s, published_time = %s, 
                expiration = %s, comment = %s
            WHERE coupon_uid = %s;
        """
        self.db.execute(query, (coupon.user_1_uid, coupon.user_2_uid, coupon.item_list, 
                                coupon.published_time, coupon.expiration, 
                                coupon.comment, coupon.coupon_uid))

    def delete_coupon(self, coupon_uid):
        query = "DELETE FROM coupons WHERE coupon_uid = %s;"
        self.db.execute(query, (coupon_uid,))
