from kafka import KafkaConsumer
import json
from models.client import RequestClient

class RequestObserver:
    def __init__(self, db:RequestClient):
        self.db = db
        self.consumer = KafkaConsumer('request-updates', 
                                       bootstrap_servers='localhost:9092',
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        
    def start_listening(self):
        for message in self.consumer:
            self.handle_message(message.value)

    def handle_message(self, message):
        request_id = message['request_id']
        new_state = message['state']

        # Get the user_id associated with this request
        user_id = self.db.get_user_id_by_request(request_id)

        if user_id:
            self.notify_user(user_id, request_id, new_state)


    def notify_user(self, user_id, request_id, new_state):
        self.db.update_request_state(user_id, request_id, new_state)

        # Notify the user via email, push notification, etc.
        self.send_notification(user_id, request_id, new_state)

    def send_notification(self, user_id, request_id, new_state):
        # Here you would put your code to send a notification to the user.
        # This could involve calling an email service, a push notification service, etc.
        print(f"Sending notification to user {user_id} about request {request_id}")
