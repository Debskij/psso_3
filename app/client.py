from app import Server
from app.auction import Auction

class Client:
    def __init__(self, username: str, binded_server: Server) -> None:
        self.username = username
        self.server = binded_server

    def update_view(self):
        auctions = self.server.get_items()

    def start_view(self):
        pass

    def notify(self, auction: Auction):
        pass