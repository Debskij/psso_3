from abc import ABC, abstractmethod

from app.server.auction_server import AuctionServer
from app.server.server import Server


class AbstractAuctionServerFactory(ABC):
    """
    The Abstract Factory for AuctionServers.
    """

    @abstractmethod
    def create_server(self) -> AuctionServer:
        pass


class AuctionServerFactory(AbstractAuctionServerFactory):
    """
    Implement the operations to create concrete servers objects.
    """

    def create_server(self):
        return Server()
