import Pyro4

from app.server.auction_server import AuctionServer
from app.client.auction_listener import AuctionListener
from app.server.auction.item import Item

@Pyro4.expose
class Server(AuctionServer):
    def __init__(self) -> None:
        super().__init__()
        self.items = dict()
        self.clients = dict()

    def add_client(self, client_name: str, client_listener: AuctionListener):
        self.clients[client_name] = client_listener
    
    def show_clients(self):
        return self.clients

    def place_item_for_bid(self, owner_name: str, item_name: str, item_desc: str,
                           start_bid: float, auction_time: int) -> None: 
        if owner_name in self.clients.keys():
            owner_listener = self.clients[owner_name]
        if item_name not in self.items.keys():
            self.items[item_name] = Item(owner_name, owner_listener, item_name, item_desc, start_bid, auction_time)

    def bid_on_item(self, bidder_username: str, item_name: str, bid: float) -> bool:
        if bidder_username in self.clients.keys():
            bidder_listener = self.clients[bidder_username]
        if item_name in self.items.keys():
            self.items[item_name].bid_on_item(bidder_username, bidder_listener, bid)

    def get_items(self) -> tuple:
        return ("dupa", "dupa")
        # return (item.parse_item for item in self.items.values())

    def register_listener(self, al: AuctionListener, item_name: str):
        if item_name in self.items.keys():
            self.items[item_name].add_observer(al)
