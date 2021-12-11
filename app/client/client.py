import Pyro4
from threading import Thread
from tkinter import *
import base64
from tkinter import ttk
import pickle

from app.client.auction_listener import AuctionListener
from app.server.server import Server
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
        auction_server: Server = Pyro4.Proxy(uri)
        self.assigned_server = auction_server
        self.daemon_thread = Thread(target=daemon.requestLoop)
        self.daemon_thread.daemon = True
        self.daemon_thread.start()

        print('polaczylem z serwerem')
        auction_server.add_client(self.username, client_uri)
        print('dodalem clienta')

    def kill_daemon(self):
        raise SystemExit

    def open_gui(self):
        root = Tk()
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        frm.master.title("Client")
        items = self.assigned_server.get_items()
        print(items)

        for idx_x, value in enumerate(items[0].keys()):
            w = Text(root, width=15, height=5)
            w.grid(row=0, column=idx_x)
            w.insert(END, value)
        for idx_y, item in enumerate(items):
            for idx_x, value in enumerate(item.values()):
                w = Text(root, width=15, height=5)
                w.grid(row=idx_y + 1, column=idx_x)
                w.insert(END, value)
            ttk.Button(root, text='bid', command=lambda: self.bid_item(item['item_name'], 100000, frm)).grid(row=idx_y + 1, column=len(item.values()))
        root.mainloop()

    def bid_item(self, item_name, new_bid, frame):
        print('tu wchodzi jeszcze')
        self.assigned_server.bid_on_item(self.username, item_name, new_bid)
        frame.update_idletasks()

    def update(self, item: bytes = None):
        print('in update')
        if item is not None:
            print(base64.b64decode(item['data']))
            item_obj: Item = pickle.loads(base64.b64decode(item['data']))
            print(f'{item_obj.item_name}')
        print('update end')

    def __str__(self):
        return self.username

    def __hash__(self):
        return hash(str(self.username))

    def __eq__(self, other):
        return hash(str(self.username)) == hash(str(other.username))
