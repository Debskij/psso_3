from abc import ABC, abstractmethod
from app.server.auction.item import Item

class AuctionListener(ABC):
    @abstractmethod
    def update(self, item: Item):
        """
        Invoked by the AuctionServer for each AuctionListener
        which has registered to be notified of changes in the
        bid status of the specified item.
        """
        raise NotImplementedError
