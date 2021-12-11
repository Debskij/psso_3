import Pyro4
import sys

from app.server.server import Server
from app.client.client import Client
from app.server.server_factory import AuctionServerFactory

ns = Pyro4.locateNS()
daemon = Pyro4.Daemon()

factory = AuctionServerFactory()
server = factory.create_server()
server1 = factory.create_server()
print(server)
print(server1)
server_uri = daemon.register(server)
ns.register(f'default.server', server_uri)
daemon.requestLoop()
