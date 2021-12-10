import Pyro4
from threading import Thread
from tkinter import *
from tkinter import ttk

from app.client.auction_listener import AuctionListener
from app.server.auction_server import AuctionServer
from app.server.auction.item import Item

@Pyro4.expose
class Client(AuctionListener):
    def __init__(self, username: str) -> None:
        self._max_bid = 100
        self.username = username
        self.daemon_thread = None

    def register_client(self, server_namespace: str = 'default.server'):
        ns = Pyro4.locateNS()
        daemon = Pyro4.Daemon()
        client_uri = daemon.register(self)
        ns.register(f'default.client.{self.username}', client_uri)
        print('zarejestrowalem klienta')
        uri = ns.lookup(server_namespace)
        auction_server: AuctionServer = Pyro4.Proxy(uri)
        self.assigned_server = auction_server
        print('polaczylem z serwerem')
        auction_server.add_client(self.username, client_uri)
        print('dodalem clienta')
        self.daemon_thread = Thread(target=daemon.requestLoop)
        self.daemon_thread.daemon = True
        self.daemon_thread.start()
    
    def kill_daemon(self):
        raise SystemExit

    def open_gui(self):
        root = Tk()
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        frm.master.title("Elo byku")
        frm.master.maxsize(1000, 400)
        ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
        ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
        root.mainloop()

    def update(self):
        print(self.assigned_server.get_items())

    def dupa(self):
        return "dziala hehe"
