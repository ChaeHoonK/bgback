# models/coupon_client.py
from sql.client import Client
from models.coupon import Coupon

class CouponClient:
    def __init__(self, client: Client):
        self.db = client

    def create_coupon(self, coupon: Coupon):
        query = """
            INSERT INTO coupons (
                coupon_uid, user_1_uid, user_2_uid, item_list, published_time, expiration, comment
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, (coupon.coupon_uid, coupon.user_1_uid, coupon.user_2_uid, 
                                coupon.item_list, coupon.published_time, coupon.expiration, 
                                coupon.comment))
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
