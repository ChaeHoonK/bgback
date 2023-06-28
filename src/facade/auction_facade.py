# facade/auction_facade.py
from models.auction import Auction, AuctionClient
from models.request import Request, RequestClient
from sql.client import ClientConnector
from facade.coupon_facade import CouponFacade



class AuctionFacade:
    def __init__(self):
        pass

    def create_auction(self, **kwargs):
        tmp = tuple(kwargs.values())
        with ClientConnector() as client:
            auction_client = AuctionClient(client)
            return auction_client.create(*tmp)

    def create_request(self, **kwargs):
        tmp = tuple(kwargs.values())
        with ClientConnector() as client:
            request_client = RequestClient(client)
            return request_client.create(*tmp)    
        

    def process_request(self, **kwargs ):
        request = None

        with ClientConnector() as client:
            request_client = RequestClient(client)
            auction_client = AuctionClient(client)
            request = request_client.get(kwargs['request_uid'])
            if kwargs['status'] == 1:
                request_reversed = Request(kwargs)
                request_reversed.reverse()
                request_client.create(request_reversed.before_creation())

            else:                
                self._finalize_auction(request)
                auction_client.delete(kwargs['auction_uid'])

            request_client.update_request_status(request['request_uid'], kwargs['status'])
            

        #notify receiver kwargs["re"]

        return request
    
    def _finalize_auction(self, request:Request):
        if request.status == 1: # approved
            self._create_coupon()


    def _create_coupon(self, request: Request):
        return CouponFacade().create_coupon(request)


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

            auction = auction_client.get(request.auction_uid)
            if auction:
                auction_client.delete(auction.auction_uid)
