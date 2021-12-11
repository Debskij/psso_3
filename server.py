import Pyro4
import sys

from app.server.server import Server
from app.client.client import Client


ns = Pyro4.locateNS()
daemon = Pyro4.Daemon()

server = Server()
server_uri = daemon.register(server)
ns.register(f'default.server', server_uri)
daemon.requestLoop()
