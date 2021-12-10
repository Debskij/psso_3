import Pyro4
import sys
from multiprocessing import Process, freeze_support

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
try:
    client = Client('janusz')
    client.register_client()
    client.update()
# client.open_gui()
except Exception as e:
    print(e)
finally:
    client.kill_daemon()
# with Pyro4.Daemon() as daemon:
#     client_uri = daemon.register(client)
#     print(client_uri)
#     with Pyro4.locateNS() as ns:
#         ns.register('default.client.testowy', client_uri)
#     print('stary wstal')
#     daemon.requestLoop()