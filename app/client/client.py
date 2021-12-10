import Pyro4

from app.client.auction_listener import AuctionListener
from app.server.auction_server import AuctionServer
from app.server.auction.item import Item


@Pyro4.expose
class Client(AuctionListener):
    def __init__(self) -> None:
        self._max_bid = 100
        self.assigned_server = None

    def assign_server(self, auction_server: AuctionServer):
        self.assigned_server = auction_server

    def update(self, item: Item):
        print(f'{item.parse_item()}')

    def dupa(self):
        return "dziala hehe"
