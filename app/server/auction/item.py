class Item:
    def __init__(self, owner_name: str, owner_observer, item_name: str, item_desc: str,
                 start_bid: float, seconds_till_end: int):
        self.owner_name = owner_name
        self.item_name = item_name
        self.item_desc = item_desc
        self.current_bid = start_bid
        self.current_bid_owner = None
        self.end_auction_time = seconds_till_end
        self.observers = {owner_name: owner_observer}

    def bid_on_item(self, bidder_username: str, bidder_observer, bid: float) -> bool:
        if bidder_username != self.owner_name and float("%.2f" % bid) > self.current_bid:
            self.current_bid = float("%.2f" % bid)
            self.current_bid_owner = bidder_username
            self.add_observer(bidder_username, bidder_observer)
            return True
        return False

    def add_observer(self, observer_name: str, observer_listener) -> bool:
        if observer_name not in self.observers.keys():
            self.observers[observer_name] = observer_listener
            return True
        return False

    def remove_observer(self, observer) -> bool:
        if observer in self.observers:
            self.observers.remove(observer)
            return True
        return False

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update(self)

    def parse_item(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "item_name": self.item_name,
            "item_desc": self.item_desc,
            "current_bid": self.current_bid,
            "current_bid_owner": self.current_bid_owner,
            "end_auction_time": self.end_auction_time
        }
