from models.table import Table
from sql.client import Client

class Wallet(Table):
    def __init__(self, wallet_uid, owner, ordinary_coupons=None,
                 discount_coupons=None, point_coupons=None):
        self.wallet_uid = wallet_uid
        self.owner = owner
        self.ordinary_coupons = ordinary_coupons or []
        self.discount_coupons = discount_coupons or []
        self.point_coupons = point_coupons or []

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS wallets (
    wallet_uid SERIAL PRIMARY KEY,
    owner  INTEGER REFERENCES users(user_uid),
    ordinary_coupons INTEGER[],
    discount_coupons INTEGER[],
    point_coupons INTEGER[]
);
        """



class WalletClient:
    def __init__(self):
        self.db = Client()

    def create_wallet(self, *args):
        query = """
            INSERT INTO wallets (
                wallet_uid, owner, ordinary_coupons, discount_coupons, point_coupons
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s);
        """
        self.db.execute(query, args)

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