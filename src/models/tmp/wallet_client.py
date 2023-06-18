from sql.client import Client
from models.wallet import Wallet

class WalletClient:
    def __init__(self):
        self.db = Client()

    def create_wallet(self, owner, ordinary_coupons, discount_coupons, point_coupons):
        query = """
            INSERT INTO wallets (
                wallet_uid, owner, ordinary_coupons, discount_coupons, point_coupons
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s);
        """
        self.db.execute(query, (owner, ordinary_coupons,
                                discount_coupons, point_coupons))

    def get_wallet(self, wallet_uid):
        query = "SELECT * FROM wallets WHERE wallet_uid = %s;"
        result = self.db.execute(query, (wallet_uid,), fetch_one=True)
        if result:
            return Wallet(*result)
        return None

    def update_wallet(self, wallet):
        query = """
            UPDATE wallets SET 
                owner = %s, ordinary_coupons = %s, discount_coupons = %s, point_coupons = %s
            WHERE wallet_uid = %s;
        """
        self.db.execute(query, (wallet.owner, wallet.ordinary_coupons, wallet.discount_coupons,
                                wallet.point_coupons, wallet.wallet_uid))

    def delete_wallet(self, wallet_uid):
        query = "DELETE FROM wallets WHERE wallet_uid = %s;"
        self.db.execute(query, (wallet_uid,))