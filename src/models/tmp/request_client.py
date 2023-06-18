from sql.client import Client
from models.request import Request

class RequestClient:
    def __init__(self, client: Client):
        self.db = client

    def create_request(self, auction_uid, receiver_user_uid, receiver_item_list,receiver_price_list,sender_user_uid,sender_item_list, sender_price_list,status=0):
        query = """
            INSERT INTO requests (
                request_uid, auction_uid, receiver_user_uid, receiver_item_list, receiver_price_list, sender_user_uid, sender_item_list, sender_price_list, status
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        result = self.db.query(query, (auction_uid, receiver_user_uid, receiver_item_list, receiver_price_list,
                                sender_user_uid, sender_item_list,sender_price_list, status), fetch_one=True)
        
        if result:
            return Request(*result)

    def get_request(self, request_uid):
        query = "SELECT * FROM requests WHERE request_uid = %s;"
        result = self.db.execute(query, (request_uid,), fetch_one=True)
        if result:
            return Request(*result)
        return None
    
    def get_user_id_by_request(self, request_id):
        # Query the database for the user_id associated with this request_id
        query = "SELECT user_id FROM requests WHERE request_id = %s;"
        result = self.db.query(query, (request_id,), fetch_one=True)

        if result:
            return result[0]
        
        return None

    def update_request(self, request: Request):
        query = """
            UPDATE requests SET 
                receiver_user_uid = %s, receiver_item_list = %s, sender_user_uid = %s, sender_item_list = %s, status = %s
            WHERE request_uid = %s;
        """
        self.db.execute(query, (request.receiver_user_uid, request.receiver_item_list, request.sender_user_uid,
                                request.sender_item_list, request.status, request.request_uid))

    def update_request_status(self, user_id, request_id, new_status):
        # Update the request state in the database
        query = """
            UPDATE requests SET 
                state = %s
            WHERE request_id = %s;
        """
        self.db.execute(query, (new_status, request_id))

    def delete_request(self, request_uid):
        query = "DELETE FROM requests WHERE request_uid = %s;"
        self.db.execute(query, (request_uid,))