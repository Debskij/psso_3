import datetime
import pickle
from app.client.auction_listener import AuctionListener
from app.server.auction.observable import Observable


class Item(Observable):
    def __init__(self, owner_name: str, item_name: str, item_desc: str, start_bid: float, seconds_till_end: int):
        super().__init__()
        self.owner_name = owner_name
        self.item_name = item_name
        self.item_desc = item_desc
        self.current_bid = start_bid
        self.end_auction_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds_till_end)

        self.current_bid_owner: str = None
        self.observers: set[AuctionListener] = set()
        print(f'Created item: {item_name}')

    def bid_on_item(self, bidder_username: str, observer: AuctionListener, bid: float) -> bool:
        new_bid = float("%.2f" % bid)
        if bidder_username != self.owner_name and new_bid > self.current_bid:
            self.current_bid = new_bid
            self.current_bid_owner = bidder_username
            self.add_observer(observer)
            self.notify_observers()
            print(f'Bid on item {self.item_name} - new price {self.current_bid}')
            return True
        print(f'Bid on item {self.item_name} unsuccessful')
        return False

    def add_observer(self, observer: AuctionListener):
        self.observers.add(observer)

    def notify_observers(self):
        for observer in self.observers:
            print(f'notify_observers: {observer}')
            try:
                observer.update(pickle.dumps(self))
            except:
                pass

    def parse_item(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "item_name": self.item_name,
            "item_desc": self.item_desc,
            "current_bid": self.current_bid,
            "end_auction_time": self.end_auction_time
        }
