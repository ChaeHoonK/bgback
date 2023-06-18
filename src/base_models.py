from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class Auction(BaseModel):
    publisher_uid:int
    item_list:list[int]
    price_list:list[int]
    wish_list:list[int]


class Request(BaseModel):
    auction_uid:int
    receiver_user_uid:int
    receiver_item_list:list[int]
    receiver_price_list:list[int]
    sender_user_uid:int
    sender_item_list:list[int]
    sender_price_list:list[int]

class RequestStatus(BaseModel):
    request_uid:int
    status:int
    auction_uid:Optional[list[int]]
    receiver_user_uid:Optional[int]
    receiver_item_list:Optional[list[int]]
    receiver_price_list:Optional[list[int]]
    sender_user_uid:Optional[int]
    sender_item_list:Optional[list[int]]
    sender_price_list:Optional[list[int]]
