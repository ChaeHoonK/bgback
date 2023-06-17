# models/request.py
from models.table import Table

class Request(Table):
    def __init__(self, request_uid, receiver_user_uid, receiver_item_list=None,
                 sender_user_uid=None, sender_item_list=None, status=None):
        self.request_uid = request_uid
        self.receiver_user_uid = receiver_user_uid
        self.receiver_item_list = receiver_item_list or []
        self.sender_user_uid = sender_user_uid
        self.sender_item_list = sender_item_list or []
        self.status = status

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS requests (
    request_uid SERIAL PRIMARY KEY,
    receiver_user_uid INTEGER REFERENCES users(user_uid),
    receiver_item_list INTEGER[],
    sender_user_uid INTEGER REFERENCES users(user_uid),
    sender_item_list INTEGER[],
    status INTEGER
);
        """
