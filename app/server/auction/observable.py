from abc import ABC, abstractmethod
from app.client.auction_listener import AuctionListener


class Observable(ABC):
    def __init__(self):
        self.observers: list[AuctionListener] = []
    
    def add_observer(self, observer: AuctionListener):
        print('added observer')
        if observer not in self.observers:
            self.observers.append(observer)
    
    @abstractmethod
    def notify_observers(self):
        raise NotImplementedError
