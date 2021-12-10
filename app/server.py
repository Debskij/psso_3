from app import Auction, Client
from datetime import datetime

class Server:
    def __init__(self) -> None:
        self.auctions = list()
        self.clients = list()
        self.soonest_ending_auction = None
    
    def get_items(self) -> list:
        return self.auctions

    def find_client_by_username(self, searched_username: str) -> Client:
        for client in self.clients:
            if client.username == searched_username:
                return client
        return None
    
    def find_auction_by_name(self, searched_item_name: str) -> Auction:
        for auction in self.auctions:
            if auction.item_name == searched_item_name:
                return auction
        return None
    
    def add_observer(self, auction_name: str, client_username: str) -> bool:
        auction = self.find_auction_by_name(auction_name)
        client = self.find_client_by_username(client_username)
        if auction is not None and client is not None:
            auction.add_observer(client)
            return True
        return False
    
    def bid_on_item(self, bidder_username: str, item_name: str, bid: float) -> bool:
        auction = self.find_auction_by_name(item_name)
        bidder = self.find_client_by_username(bidder_username)
        if item_name is not None and bidder is not None and bidder != auction.owner:
            auction.bid_on_item(bid)
            client

        

    def create_auction(self, owner_username: str, item_name: str, item_desc: str, start_bid: float, auction_time: datetime) -> bool:
        auction_owner = self.find_client_by_username(owner_username)
        existing_auction = self.find_auction_by_name(item_name)
        if auction_owner is None or existing_auction is not None:
            return False
        new_auction = Auction(auction_owner, item_name, item_desc, start_bid, auction_time)
        self.auctions.append(new_auction)
        return True

    def register_client(self, username: str) -> True:
        if self.find_client_by_username(username) is None:
            new_client = Client(username, self)
            self.clients.append(new_client)
            new_client.start_view()
            return True
        return False

