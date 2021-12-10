from app import  Client

from datetime import datetime

class Auction:
    def __init__(self, owner: Client, item_name: str, item_desc: str, start_bid: float, auction_time: datetime) -> None:
        self.owner = owner
        self.item_name = item_name
        self.item_desc = item_desc
        self.current_bid = start_bid
        self.current_bid_owner = None
        self.end_auction_time = auction_time
        self.observers = {owner}

    def bid_on_item(self, bidder: Client, bid: float) -> list:
        return self.observers()

    def add_observer(self, observer: Client) -> bool:
        if observer in self.observers:
            self.observers.add(observer)
            return True
        return False

    def remove_observer(self, observer: Client) -> bool:
        if observer in self.observers:
            self.observers.remove(observer)
            return True
        return False
    
    def notify_observers(self, message_type):
        for observer in self.observers:
            observer.notify(message_type)