import datetime
from app.server.auction.observable import Observable


class Item(Observable):
    def __init__(self, owner_name: str, item_name: str, item_desc: str, start_bid: float, seconds_till_end: int):
        super().__init__()
        self.owner_name = owner_name
        self.item_name = item_name
        self.item_desc = item_desc
        self.current_bid = start_bid
        self.end_auction_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds_till_end)
        self.current_bid_owner = None
        print('item')

    def bid_on_item(self, bidder_username: str, observer, bid: float) -> bool:
        print('item')
        if bidder_username != self.owner_name and float("%.2f" % bid) > self.current_bid:
            print('bid_on_item - jestem w item')
            self.current_bid = float("%.2f" % bid)
            self.current_bid_owner = bidder_username
            self.add_observer(observer)
            self.notify_observers()
            return True
        return False

    def parse_item(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "item_name": self.item_name,
            "item_desc": self.item_desc,
            "current_bid": self.current_bid,
            "end_auction_time": self.end_auction_time
        }

    def notify_observers(self):
        for observer in self.observers:
            print('notify_observers')
            observer.update()
            print('after update notify_observers')
