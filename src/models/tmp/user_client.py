from sql.client import Client
from models.user import User

#models/user_client.py
class UserClient:
    def __init__(self, client:Client, user:User=None):
        self.db = client
        self.user = user

    def create(self, email, password,second_password, phone_number,second_phone_number,wallet_id,store_uids):
        try:
            query = """
            INSERT INTO Users (
                email, password, second_password, phone_number, second_phone_number, wallet_id, store_uids
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """
            result = self.db.query(query, (email, password, second_password, phone_number,second_phone_number,wallet_id,store_uids ))
            return User(*result)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get(self, userUID):
        try:
            query = "SELECT * FROM Users WHERE userUID = %s;"
            result = self.db.query(query, (userUID,))
            if result:
                return User(*result)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_by_id(self, userUID):
        self.user = self.get(userUID)

    def set_user(self, user: User):
        self.user = user

    def update(self, userUID, ID, PW, second_PW, storeUID, phone, wallet):
        try:
            query = """
            UPDATE Users SET 
                ID = %s, PW = %s, second_PW = %s, storeUID = %s, phone = %s, wallet = %s
            WHERE userUID = %s;
            """
            self.db.execute(query, (ID, PW, second_PW, storeUID, phone, wallet, userUID))
            self.db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, userUID):
        try:
            query = "DELETE FROM Users WHERE userUID = %s;"
            self.db.execute(query, (userUID,))
            self.db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
