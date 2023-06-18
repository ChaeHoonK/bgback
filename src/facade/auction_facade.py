# facade/auction_facade.py
from models.auction import Auction, AuctionClient
from models.request import Request, RequestClient
from sql.client import ClientConnector
from models.coupon import Coupon, CouponClient


class AuctionFacade:
    def __init__(self):
        pass

    def create_auction(self, **kwargs):
        tmp = tuple(kwargs.values())
        with ClientConnector() as client:
            auction_client = AuctionClient(client)
            return auction_client.create_auction(*tmp)

    def create_request(self, **kwargs):
        tmp = tuple(kwargs.values())
        with ClientConnector() as client:
            request_client = RequestClient(client)
            return request_client.create_request(*tmp)    
        

    def process_request(self, **kwargs ):
        request = None

        with ClientConnector() as client:
            request_client = RequestClient(client)
            auction_client = AuctionClient(client)
            if kwargs['status'] == 0:
                request = Request(kwargs)
            else:                
                request = auction_client.get_auction()
                self._finalize_auction(request)

            request_client.update_request(request)

        #notify receiver kwargs["re"]

        return request
    
    def _finalize_auction(self, request:Request):
        if request.status == 1: # approved
            self._create_coupon()


    def _create_coupon(self, request: Request):
        pass


    def _finalize_transaction(self, request: Request):
        """
        Facade method for finalizing a transaction. 
        It assumes that the transaction is finalized when a request is accepted.
        
        Arguments:
        request: Request object to be finalized

        Returns:
        None
        """
        if request.status != 1:  # not accepted
            print('The request is not accepted.')
            return

        with ClientConnector() as client:
            auction_client = AuctionClient(client)

            # finalize the transaction
            # e.g., delete the auction, update the items of the users, etc.
            # the details of the transaction finalization are omitted for brevity

            auction = auction_client.get_auction(request.auction_uid)
            if auction:
                auction_client.delete_auction(auction.auction_uid)
