from abc import ABC, abstractmethod


class AuctionListener(ABC):
    username: str
    @abstractmethod
    def update(self, item):
        """
        Invoked by the AuctionServer for each AuctionListener
        which has registered to be notified of changes in the
        bid status of the specified item.
        """
        raise NotImplementedError
