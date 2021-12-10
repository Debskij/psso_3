import Pyro4
import json
from app import client

from app.server.auction_server import AuctionServer
from app.client.auction_listener import AuctionListener
from app.server.auction.item import Item


@Pyro4.expose
class Server(AuctionServer):
    def __init__(self) -> None:
        super().__init__()
        self.items = dict()
        self.clients = dict()
        self.load_items()

    def add_client(self, client_name: str, client_uri):
        client: AuctionListener = Pyro4.Proxy(client_uri)
        self.clients[client_name] = client

    def show_clients(self):
        return self.clients

    def place_item_for_bid(self, owner_name: str, item_name: str, item_desc: str,
                           start_bid: float, auction_time: int) -> None:
        if owner_name in self.clients.keys():
            owner_listener = self.clients[owner_name]
        if item_name not in self.items.keys():
            self.items[item_name] = Item(
                owner_name, owner_listener, item_name, item_desc, start_bid, auction_time)

    def bid_on_item(self, bidder_username: str, item_name: str, bid: float) -> bool:
        if bidder_username in self.clients.keys():
            bidder_listener = self.clients[bidder_username]
        if item_name in self.items.keys():
            self.items[item_name].bid_on_item(
                bidder_username, bidder_listener, bid)

    def get_items(self) -> tuple:
        return [item.parse_item() for item in self.items.values()]

    def register_listener(self, al: AuctionListener, item_name: str):
        if item_name in self.items.keys():
            self.items[item_name].add_observer(al)

    def load_items(self):
        file = open('C:\\Users\\debsk\\Documents\\GitHub\\psso_3\\app\\data\\items.json')
        data = json.load(file)
        for item_data in data:
            self.items[item_data['item_name']] = Item(item_data['owner_name'],
                                                      item_data['item_name'],
                                                      item_data['item_desc'],
                                                      item_data['start_bid'],
                                                      item_data['seconds_till_end'])
        file.close()
