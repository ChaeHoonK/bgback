from sql.client import Client
from models.user import User

class UserClient:
    def __init__(self, client:Client, user:User=None):
        self.client = client
        self.user = user

    def create(self, ID, PW,second_PW, storeUID,phone,wallet):
        try:
            self.client.cursor.execute("INSERT INTO Users VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)", (ID, PW, storeUID,second_PW, phone, wallet))
            self.client.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, userUID):
        try:
            self.client.cursor.execute("SELECT * FROM Users WHERE userUID = %s", (userUID,))
            return self.client.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_by_id(self, userUID):
        try:
            self.client.cursor.execute("SELECT * FROM Users WHERE userUID = %s", (userUID,))
            self.user = User(*self.client.cursor.fetchone())
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def set_user(self, user: User):
        self.user = user

    def update(self, userUID, ID, PW, storeUID, phone, wallet):
        try:
            self.client.cursor.execute("UPDATE Users SET ID = %s, PW = %s, storeUID = %s, phone = %s, wallet = %s WHERE userUID = %s", (ID, PW, storeUID, phone, wallet, userUID))
            self.client.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

   #_memoizing and caching in python
    def delete(self, userUID):
        try:
            self.client.cursor.execute("DELETE FROM Users WHERE user = %s", (userUID,))
            self.client.commit()
        except Exception as e:
            print(f"An error occurred: {e}")