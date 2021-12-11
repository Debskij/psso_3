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
        def refresh():
            pass
        def bid(item_name: str, entries_boxes: dict, grid_fields: dict):
            print(item_name, entries_boxes[item_name].get())
            for key, entry in entries_boxes.items():
                print(key, entry.get())
            new_price = float(entries_boxes[item_name].get())
            self.bid_item(item_name, new_price)
            # grid_fields[item_name]['current_bid'].configure(text=str(new_price))

        root = Tk()
        root.title('Auction Client')
        canvas = Canvas(root, width=700, height=1200, relief='raised')
        canvas.pack()
        frm = Frame(canvas)
        frm.grid()
        self.items = self.assigned_server.get_items()
        entries = dict()
        buttons = list()
        grid_fields = dict()
        for idx_x, value in enumerate(self.items[0].keys()):
            w = Text(canvas, width=15, height=5)
            w.grid(row=0, column=idx_x)
            w.insert(END, value)
            w["state"] = DISABLED
        for idx_y, item in enumerate(self.items):
            grid_fields[item['item_name']] = dict()
            for idx_x, (field_name, value) in enumerate(item.items()):
                w = Text(canvas, width=15, height=5)
                w.grid(row=idx_y + 1, column=idx_x)
                w.insert(END, value)
                w["state"] = DISABLED
                grid_fields[item['item_name']][field_name] = w
            entry = Entry(canvas)
            item_name_copy = str(self.items[idx_y]['item_name'])
            entries[str(item['item_name'])] = entry
            entry.grid(row=idx_y + 1, column=len(item.values()))
            buttons.append(Button(canvas, text='bid', command=lambda name=item_name_copy: bid(name, entries, grid_fields)))
            buttons[idx_y].grid(row=idx_y + 1, column=len(item.values())+1)
        root.mainloop()

    def bid_item(self, item_name, new_bid):
        print(f'{self.username}: {item_name} {new_bid}')
        self.assigned_server.bid_on_item(self.username, item_name, new_bid)

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
