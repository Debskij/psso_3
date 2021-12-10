import Pyro4
import sys
from time import time

from app.server.server import Server
from app.client.client import Client




sys.excepthook = Pyro4.util.excepthook

# server = Pyro4.Proxy("PYRONAME:default.server")
ns = Pyro4.locateNS()
uri = ns.lookup('default.client.janusz')
client: Client = Pyro4.Proxy(uri)
print('asd')

# daemon = Pyro4.Daemon()
# client_uri = daemon.register(Client)
# print(client_uri)
# client: Client = Pyro4.Proxy(client_uri)
print(client.dupa())

# server = Server()
# server.add_client("janusz", client)
# # # client.assign_server(server)

# # print(server.get_items())
# print(server.show_clients())