# models/coupon.py
from models.table import Table
import datetime

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
