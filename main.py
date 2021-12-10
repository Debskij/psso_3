import Pyro4
import sys

from app.server.server import Server
from app.client.client import Client



sys.excepthook = Pyro4.util.excepthook

# server = Pyro4.Proxy("PYRONAME:default.server")
client = Pyro4.Proxy("PYRONAME:default.client")

server = Server()
server.add_client("janusz", client)
# client.assign_server(server)

print(server.get_items())
print(server.show_clients())