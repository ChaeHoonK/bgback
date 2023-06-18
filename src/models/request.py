# models/request.py
from models.table import Table
from states.request_state import NewState, RequestState
from kafka import KafkaProducer
import json
from sql.client import Client

class Request(Table):
    def __init__(self, request_uid, auction_uid, receiver_user_uid, receiver_item_list=None, receiver_price_list=None,
                 sender_user_uid=None, sender_item_list=None,sender_price_list=None, status=None):
        self.request_uid = request_uid
        self.auction_uid = auction_uid
        self.receiver_user_uid = receiver_user_uid
        self.receiver_item_list = receiver_item_list or []
        self.receiver_price_list = receiver_price_list or []
        
        self.sender_user_uid = sender_user_uid
        self.sender_item_list = sender_item_list or []
        self.sender_price_list = sender_price_list or []
        self.status = status
        self.state = NewState()

    def set_state(self, state: RequestState):
        self.state = state

    def process(self):
        self.state.process_request(self)

    def notify_observers(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092', 
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send('request-updates', {'request_id': self.request_uid, 'state': self.state.name})
        producer.flush()

    @classmethod
    def _ensure_table_sql(cls) -> str:
        return """
CREATE TABLE IF NOT EXISTS requests (
    request_uid SERIAL PRIMARY KEY,
    auction_uid INTERGER REFERENCES auctions(auction_uid),
    receiver_user_uid INTEGER REFERENCES users(user_uid),
    receiver_item_list INTEGER[],
    sender_user_uid INTEGER REFERENCES users(user_uid),
    sender_item_list INTEGER[],
    status INTEGER
);
        """




class RequestClient:
    def __init__(self, client: Client):
        self.db = client

    def create_request(self, *args):
        query = """
            INSERT INTO requests (
                request_uid, auction_uid, receiver_user_uid, receiver_item_list, receiver_price_list, sender_user_uid, sender_item_list, sender_price_list, status
            ) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, 0) RETURNING *;
        """
        result = self.db.query(query, args, fetch_one=True)
        
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