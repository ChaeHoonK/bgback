from models.table import Table

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
