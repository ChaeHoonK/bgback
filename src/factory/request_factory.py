# factory/request_factory.py
from models.request import Request
from sql.client import ClientConnector
from models.request_client import RequestClient

class RequestFactory:
    def __init__(self,):
        self.request_client = None

    def create_request(self, receiver_user_uid, sender_user_uid, sender_item_list):
        """
        Factory method for creating a new request.
        
        Arguments:
        receiver_user_uid: user_uid of the receiver of the request
        sender_user_uid: user_uid of the sender of the request
        sender_item_list: a list of item_uids that the sender is willing to provide

        Returns:
        Request object
        """
        with ClientConnector() as client:
            self.request_client = RequestClient(client)
            request = Request(None, receiver_user_uid, None, sender_user_uid, sender_item_list, None)
            new_request = self.request_client.create_request(request)
            return new_request
