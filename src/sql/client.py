import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
from typing import List
from type import Coupon, User, Store, Request, Transaction, Item


class DBClient:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS']
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close: bool
        self.connection.close()

    def commit(self):
        self.connection.commit()


class UserClient:
    def __init__(self, dbclient:DBClient, user:User=None):
        self.dbclient = dbclient
        self.user = user

    def create(self):
        try:
            if self.user == None:
                raise "UserClient: user not provided"
            self.dbclient.cursor.execute("INSERT INTO Users VALUES (%s, %s, %s, %a, %s, %s)", (self.user.userUID, self.user.ID, self.user.PW, self.user.storeUID, self.user.phone, self.user.wallet))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, userUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Users WHERE userUID = %s", (userUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_by_id(self, userUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Users WHERE userUID = %s", (userUID,))
            self.user = User(*self.dbclient.cursor.fetchone())
        
        except Exception as e:
            print(f"An error occurred: {e}")


    def update(self, userUID, ID, PW, storeUID, phone, wallet):
        try:
            self.dbclient.cursor.execute("UPDATE Users SET ID = %s, PW = %s, storeUID = %s, phone = %s, wallet = %s WHERE userUID = %s", (ID, PW, storeUID, phone, wallet, userUID))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

   #_memoizing and caching in python
    def delete(self, userUID):
        try:
            self.dbclient.cursor.execute("DELETE FROM Users WHERE user = %s", (userUID,))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


class StoreClient:
    def __init__(self, dbclient:DBClient, store:Store=None):
        self.dbclient = dbclient
        self.store = store

    def create(self):
        try:
            if self.store == None:
                raise "UserStore: store not provided"
            self.dbclient.cursor.execute("INSERT INTO Stores VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (self.store.storeUID, self.store.phone, self.store.name, self.store.latitude, self.store.longitude, self.store.address, self.store.menus, self.store.urls))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, storeUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Stores WHERE storeUID = %s", (storeUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, storeUID, phone, name, latitude, longitude, address, menus, urls):
        try:
            self.dbclient.cursor.execute("UPDATE Stores SET phone = %s, name = %s, latitude = %s, longitude = %s, address = %s, menus = %s, urls = %s WHERE storeUID = %s", (phone, name, latitude, longitude, address, menus, urls, storeUID))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, storeUID):
        try:
            self.dbclient.cursor.execute("DELETE FROM Stores WHERE storeUID = %s", (storeUID,))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

class ItemClient:
    def __init__(self, dbclient:DBClient, item:Item=None):
        self.dbclient = dbclient
        self.item = item

    def create(self):
        try:
            if self.item == None:
                raise 'ItemClient: item not provided'
            self.dbclient.cursor.execute("INSERT INTO Items VALUES (%s, %s, %s, %s, %s)", (self.item.itemUID, self.item.name, self.item.category1, self.item.category2, self.item.category3))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, itemUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Items WHERE itemUID = %s", (itemUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, itemUID, name, category1, category2, category3):
        try:
            self.dbclient.cursor.execute("UPDATE Items SET name = %s, category1 = %s, category2 = %s, category3 = %s WHERE itemUID = %s", (name, category1, category2, category3, itemUID))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, itemUID):
        try:
            self.dbclient.cursor.execute("DELETE FROM Items WHERE itemUID = %s", (itemUID,))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

class TransactionClient:
    def __init__(self, dbclient:DBClient,transaction:Transaction=None):
        self.dbclient = dbclient
        self.transaction = transaction

    def create(self):
        try:
            if self.transaction == None:
                raise "TransactionClient: transaction not provided"
            self.dbclient.cursor.execute("INSERT INTO transactions (timestamp, couponUID, clientID, hostID) VALUES (%s, %s, %s, %s)", 
                            (self.transaction.timestamp, self.transaction.couponUID, self.transaction.clientID, self.transaction.hostID))
            self.dbclient.commit()
            print("Transaction added successfully")
        except Exception as e:
            print(f"Failed to add transaction: {e}")
        
    def get(self, transactionUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM transactions WHERE transactionUID = %s", (transactionUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"Failed to get transaction: {e}")

    def update(self):
        try:
            self.dbclient.cursor.execute("UPDATE transactions SET timestamp = %s, couponUID = %s, clientID = %s, hostID = %s WHERE transactionUID = %s", 
                            (self.timestamp, self.couponUID, self.clientID, self.hostID, self.transactionUID))
            self.dbclient.commit()
            print("Transaction updated successfully")
        except Exception as e:
            print(f"Failed to update transaction: {e}")

    def delete(self, transactionUID):
        cursor = self.dbclient.cursor()
        try:
            cursor.execute("DELETE FROM transactions WHERE transactionUID = %s", (transactionUID,))
            self.dbclient.commit()
            print("Transaction deleted successfully")
        except Exception as e:
            print(f"Failed to delete transaction: {e}")


class CouponClient:
    def __init__(self, dbclient:DBClient, coupon:Coupon=None):
        self.dbclient = dbclient
        self.coupon = coupon

    def create(self):
        try:
            if self.coupon == None:
                raise "Coupon"
            self.dbclient.cursor.execute("INSERT INTO Coupons VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                         (self.coupon.couponUID, self.coupon.user1_UID, self.coupon.user2_UID, self.coupon.itemList, self.coupon.published_time, self.coupon.expiration, self.coupon.comment))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def read(self, couponUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Coupons WHERE couponUID = %s", (couponUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_by_id(self, userUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Coupons WHERE userUID = %s", (userUID,))
            self.user = Coupon(*self.dbclient.cursor.fetchone())
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, couponUID, user1_UID, user2_UID, itemList, published_time, expiration, comment):
        try:
            self.dbclient.cursor.execute(
                "UPDATE Coupons SET user1_UID = %s, user2_UID = %s, itemList = %s, published_time = %s, expiration = %s, comment = %s WHERE couponUID = %s",
                (user1_UID, user2_UID, itemList, published_time, expiration, comment, couponUID))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, couponUID):
        try:
            self.dbclient.cursor.execute("DELETE FROM Coupons WHERE couponUID = %s", (couponUID,))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


class RequestClient:
    def __init__(self, dbclient:DBClient, request:Request=None):
        self.dbclient = dbclient
        self.request = request

    def create(self):
        try:

            self.dbclient.cursor.execute(
                "INSERT INTO Requests (from_userUID, from_itemList, to_userUID, to_itemList, status) VALUES (%s, %s, %s, %s, %s)", 
                (self.request.sender, self.request.sender_items, self.request.receiver, self.request.receiver_items, self.request.status)
            )
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


    def read(self, requestUID):
        try:
            self.dbclient.cursor.execute("SELECT * FROM Requests WHERE requestUID = %s", (requestUID,))
            return self.dbclient.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")

    def update(self, requestUID, from_userUID, from_itemList, to_userUID, to_itemList, status):
        try:
            self.dbclient.cursor.execute(
                "UPDATE Requests SET from_userUID = %s, from_itemList = %s, to_userUID = %s, to_itemList = %s, status = %s WHERE requestUID = %s",
                (from_userUID, from_itemList, to_userUID, to_itemList, status, requestUID))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete(self, requestUID):
        try:
            self.dbclient.cursor.execute("DELETE FROM Requests WHERE requestUID = %s", (requestUID,))
            self.dbclient.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


