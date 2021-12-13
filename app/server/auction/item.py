import datetime
import pickle
from app.client.auction_listener import AuctionListener
from app.logger import create_logger
from app.server.auction.observable import Observable


class Item(Observable):
    def __init__(self, owner_name: str,
                 owner_listener: AuctionListener,
                 item_name: str,
                 item_desc: str,
                 start_bid: float,
                 end_auction_time: datetime.datetime,
                 current_bid_owner: str = ''):

        self._logger = create_logger(f'item_{item_name}')
        self.owner_name = owner_name
        self.item_name = item_name
        self.item_desc = item_desc
        self.current_bid = float(start_bid)
        self.end_auction_time = end_auction_time
        self.current_bid_owner: str = current_bid_owner
        self.observers: set[AuctionListener] = set()
        self.add_observer(owner_listener)
        self._logger.info(f'Created item: {self.parse_item()}')

    def bid_on_item(self, bidder_username: str, observer: AuctionListener, bid: float) -> bool:
        new_bid = float("%.2f" % bid)
        if bidder_username != self.owner_name \
                and new_bid > self.current_bid \
                and datetime.datetime.now() < self.end_auction_time:
            self.current_bid = new_bid
            self.current_bid_owner = bidder_username
            self.add_observer(observer)
            self.notify_observers()
            self._logger.info(f'Bid on item {self.item_name} - new price {self.current_bid}')
            return True
        self._logger.info(f'Bid on item {self.item_name} unsuccessful')
        return False

    def add_observer(self, observer: AuctionListener):
        if observer is not None:
            self.observers.add(observer)
            self._logger.info(f'New observer added {observer}')

    def notify_observers(self):
        for observer in self.observers:
            try:
                self._logger.info(f'Notify observer: {observer}')
                observer.update(pickle.dumps(self))
            except:
                pass

    def parse_item(self, for_database_format: bool = False) -> dict:
        end_action_time = self.end_auction_time.strftime("%H:%M:%S\n%d.%m.%Y")
        if for_database_format:
            end_action_time = self.end_auction_time

        return {
            "owner_name": self.owner_name,
            "item_name": self.item_name,
            "item_desc": self.item_desc,
            "current_bid": self.current_bid,
            "current_bid_owner": self.current_bid_owner,
            "end_auction_time": end_action_time
        }
