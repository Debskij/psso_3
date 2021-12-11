from abc import ABC, abstractmethod
from app.client.auction_listener import AuctionListener


class Observable(ABC):
    @abstractmethod
    def add_observer(self, observer: AuctionListener):
        raise NotImplementedError

    @abstractmethod
    def notify_observers(self):
        raise NotImplementedError
