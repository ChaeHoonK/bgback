from sql.client import DBClient, UserClient, CouponClient
from sql.type import User

class UserManager:
    @classmethod
    def create_user(cls, ):
        pass

    def __init__(self, userId):
        self.dbclient = DBClient()
        self.userClient = UserClient(self.dbclient)
        self.userClient.set_by_id(userId)

    
    def request_trade(self, receiver,):
        pass

    def reject_trade(self, ):
        pass

    def modify_trade(self, ):
        pass

    def accept_trade(self, ):
        # Create Coupon
        pass


class CouponManager:
    @classmethod
    def create_coupon(cls, ):
        pass

    def __init__(self, couponId):
        self.dbclient = DBClient()
        self.couponClient = CouponClient(self.dbclient)
        self.couponClient.set_by_id(couponId)

    def use_coupon(self,):
        # 
        pass

    def veryfy_coupon(self,):
        pass