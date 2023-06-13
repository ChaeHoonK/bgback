from typing import List, Optional
from datetime import datetime, timedelta


class User:
    def __init__(self, userUID: int, ID: str, PW: str, store_UID: Optional[int], second_PW: str, phone: str, wallet: Optional[List[str]]):
        self.userUID = userUID
        self.ID = ID
        self.PW = PW
        self.store_UID = store_UID
        self.second_PW = second_PW
        self.phone = phone
        self.wallet = wallet if wallet is not None else []


class Store:
    def __init__(self, storeUID: int, phone: str, name: str, latitude: float, longitude: float, address: str, menus: List[(str,int)], URLs: List[str]):
        self.storeUID = storeUID
        self.phone = phone
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.menus = menus
        self.URLs = URLs


class Item:
    def __init__(self, itemUID: int, name: str, category1: str, category2: str, category3: str):
        self.itemUID = itemUID
        self.name = name
        self.category1 = category1
        self.category2 = category2
        self.category3 = category3


class Transaction:
    def __init__(self, transactionUID: int, timestamp: datetime, couponUID: int, clientID: int, hostID: int):
        self.transactionUID = transactionUID
        self.timestamp = timestamp
        self.couponUID = couponUID
        self.clientID = clientID
        self.hostID = hostID


## Realtime Data

class Coupon:
    def __init__(self, couponUID: int, user1_UID: int, user2_UID: int, itemList: List[int], published_time: datetime, expiration: datetime, comment: str):
        self.couponUID = couponUID
        self.user1_UID = user1_UID
        self.user2_UID = user2_UID
        self.itemList = itemList
        self.published_time = published_time
        self.expiration = expiration
        self.comment = comment
        self.sharable = True


class Request:
    def __init__(self, sender: int, sender_items: List[int], receiver: int, receiver_items: List[int], status: int=0, requestUID:int =None):
        self.requestUID = requestUID
        self.sender = sender
        self.sender_items = sender_items
        self.receiver = receiver
        self.receiver_items = receiver_items
        self.status = status  # 0: pending, 1:approved, 2:rejected


class Auction:
    def __init__(self, my_item: int, wish_list: List[str]):
        self.my_item = my_item
        self.wish_list = wish_list  # list of category strings


class Message:
    def __init__(self, messageUID: int, timestamp: datetime, content: str, to: int, from_: int):
        self.messageUID = messageUID
        self.timestamp = timestamp
        self.content = content
        self.to = to
        self.from_ = from_
