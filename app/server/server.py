import pymongo
import datetime
from tkinter.constants import N

import Pyro4
import Pyro4.errors
import json

from app.server.auction_server import AuctionServer
from app.client.auction_listener import AuctionListener
from app.server.auction.item import Item


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
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

        self._load_database()

    def add_client(self, client_name, client_uri):
        client = Pyro4.Proxy(client_uri)
        self.clients[client_name] = client

    def register_listener(self, al, item_name):
        if item_name in self.items.keys():
            self.items[item_name].add_observer(al)
            return self.get_items()
        raise Pyro4.errors.NamingError

    def place_item_for_bid(self, owner_name, item_name, item_desc, start_bid, auction_time):
        if owner_name in self.clients.keys():
            owner_listener = self.clients[owner_name]
            if item_name not in self.items.keys():
                self.items[item_name] = Item(owner_name, owner_listener, item_name, item_desc, start_bid,
                                             datetime.datetime.now() + datetime.timedelta(seconds=int(auction_time)))
                self._insert_record(self.items[item_name])
                return self.get_items()
        raise Pyro4.errors.NamingError

    def bid_on_item(self, bidder_username, item_name, bid):
        print(f'bid_on_item - {bidder_username}, {item_name}')
        if bidder_username in self.clients.keys():
            bidder_listener = self.clients[bidder_username]
            if item_name in self.items.keys():
                is_success = self.items[item_name].bid_on_item(bidder_username, bidder_listener, bid)
                print(self.items[item_name].parse_item())
                if is_success:
                    self._update_record(self.items[item_name])
                return is_success
        raise Pyro4.errors.NamingError

    def get_items(self):
        return [item.parse_item() for item in self.items.values()]

    def _load_database(self):
        self.db_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db_auction = self.db_client['Auction']

        # Collections
        self.coll_item = self.db_auction.get_collection('coll_item')
        self.coll_user = self.db_auction.get_collection('coll_user')

        for item_data in self.coll_item.find():
            self.items[item_data['item_name']] = Item(item_data['owner_name'],
                                                      None,
                                                      item_data['item_name'],
                                                      item_data['item_desc'],
                                                      item_data['current_bid'],
                                                      item_data['end_auction_time'],
                                                      item_data['current_bid_owner'])

    def _update_record(self, item: Item):
        self.coll_item.replace_one({"item_name": item.item_name}, item.parse_item())

    def _insert_record(self, item: Item):
        self.coll_item.insert_one(item.parse_item())
