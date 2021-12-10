import Pyro4
import sys

from app.server.server import Server
from app.client.client import Client

# Pyro4.Daemon.serveSimple(
#     {
#         Client: "default.client"
#     },
#     ns = False 
# )

# daemon = Pyro4.Daemon()
# client_uri = daemon.register(Client)
# print(client_uri)

# daemon.requestLoop()


# client = Client()
with Pyro4.Daemon() as daemon:
    client_uri = daemon.register(Client)
    print(client_uri)
    with Pyro4.locateNS() as ns:
        ns.register('default.client.testowy', client_uri)
    print('stary wstal')
    daemon.requestLoop()