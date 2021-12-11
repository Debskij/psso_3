import Pyro4
import Pyro4.errors
import json

from app.server.auction_server import AuctionServer
from app.client.auction_listener import AuctionListener
from app.server.auction.item import Item


@Pyro4.expose
class Server(AuctionServer):
    """
    Concrete auction server used to maintain a list
    of items available for auction purchase. Clients
    will be allowed to register on server and make
    bids on available items or put new items up for auction.
    """

    def __init__(self) -> None:
        self.items: dict[str, Item] = dict()
        self.clients: dict[str, AuctionListener] = dict()

        self._load_items()

    def add_client(self, client_name, client_uri):
        client = Pyro4.Proxy(client_uri)
        self.clients[client_name] = client

    def register_listener(self, al, item_name):
        if item_name in self.items.keys():
            self.items[item_name].add_observer(al)
            return self.items[item_name]
        raise Pyro4.errors.NamingError

    def place_item_for_bid(self, owner_name, item_name, item_desc, start_bid, auction_time):
        if item_name not in self.items.keys():
            self.items[item_name] = Item(owner_name, item_name, item_desc, start_bid, auction_time)
            return self.items[item_name]
        raise Pyro4.errors.NamingError

    def bid_on_item(self, bidder_username: str, item_name: str, bid: float) -> bool:
        print(f'bid_on_item - {bidder_username}, {item_name}')
        if bidder_username in self.clients.keys():
            bidder_listener = self.clients[bidder_username]
            if item_name in self.items.keys():
                is_success = self.items[item_name].bid_on_item(bidder_username, bidder_listener, bid)
                print(self.items[item_name].parse_item())
                return is_success
        raise Pyro4.errors.NamingError

    def get_items(self) -> tuple:
        return [item.parse_item() for item in self.items.values()]

    def _load_items(self):
        file = open('./data/items.json')
        data = json.load(file)
        for item_data in data:
            self.items[item_data['item_name']] = Item(item_data['owner_name'],
                                                      item_data['item_name'],
                                                      item_data['item_desc'],
                                                      item_data['start_bid'],
                                                      item_data['seconds_till_end'])
        file.close()
