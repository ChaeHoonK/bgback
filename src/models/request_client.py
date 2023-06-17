from sql.client import Client
from models.request import Request

class RequestClient:
    def __init__(self):
        self.db = Client()

    def create_request(self, receiver_user_uid, receiver_item_list,sender_user_uid,sender_item_list,status):
        query = """
            INSERT INTO requests (
                DEFAULT, receiver_user_uid, receiver_item_list, sender_user_uid, sender_item_list, status
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.db.execute(query, (receiver_user_uid, receiver_item_list,
                                sender_user_uid, sender_item_list, status))

    def get_request(self, request_uid):
        query = "SELECT * FROM requests WHERE request_uid = %s;"
        result = self.db.execute(query, (request_uid,), fetch_one=True)
        if result:
            return Request(*result)
        return None

    def update_request(self, request: Request):
        query = """
            UPDATE requests SET 
                receiver_user_uid = %s, receiver_item_list = %s, sender_user_uid = %s, sender_item_list = %s, status = %s
            WHERE request_uid = %s;
        """
        self.db.execute(query, (request.receiver_user_uid, request.receiver_item_list, request.sender_user_uid,
                                request.sender_item_list, request.status, request.request_uid))

    def delete_request(self, request_uid):
        query = "DELETE FROM requests WHERE request_uid = %s;"
        self.db.execute(query, (request_uid,))