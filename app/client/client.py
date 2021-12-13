from datetime import date, datetime, timedelta
import Pyro4
from threading import Thread
from tkinter import *
import base64
import pickle

from app.client.auction_listener import AuctionListener
from app.logger import create_logger
from app.server.server import Server
from app.server.auction.item import Item


@Pyro4.expose
class Client(AuctionListener):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.daemon_thread = None
        self.assigned_server = None
        self.minute_before = dict()
        self.outbid = dict()
        self._logger = create_logger(f'client_{username}')

    def register_client(self, server_namespace: str = 'default.server'):
        ns = Pyro4.locateNS()
        daemon = Pyro4.Daemon()
        client_uri = daemon.register(self)
        ns.register(f'default.client.{self.username}', client_uri)
        self._logger.info(f'Client registered at {client_uri} uri')

        uri = ns.lookup(server_namespace)
        auction_server: Server = Pyro4.Proxy(uri)
        self.assigned_server = auction_server
        self.daemon_thread = Thread(target=daemon.requestLoop)
        self.daemon_thread.daemon = True
        self.daemon_thread.start()
        self._logger.info(f'Client connected with server')

        auction_server.add_client(self.username, client_uri)

    def kill_daemon(self):
        self._logger.info(f'Client disconnected.')
        raise SystemExit

    def open_gui(self):
        def parse_string_to_datetime(date: str):
            return datetime.strptime(date, "%H:%M:%S\n%d.%m.%Y").replace(microsecond=0)

        def apply_strategies():
            for item_name, max_bid in self.minute_before.items():
                item_index = self.find_item(item_name)
                if (datetime.now().replace(microsecond=0) + timedelta(minutes=1)) == parse_string_to_datetime(self.items[item_index]['end_auction_time']):
                    current_price = float(self.items[item_index]['current_bid'])
                    current_highest_bidder = self.items[item_index]['current_bid_owner']
                    if current_highest_bidder != self.username and current_price < max_bid:
                        self.bid_item(item_name, min(current_price*2, max_bid))
            for item_name, max_bid in self.outbid.items():
                item_index = self.find_item(item_name)
                current_price = float(self.items[item_index]['current_bid'])
                current_highest_bidder = self.items[item_index]['current_bid_owner']
                if current_price < max_bid and current_highest_bidder != self.username and datetime.now() < parse_string_to_datetime(self.items[item_index]['end_auction_time']):
                    self.bid_item(item_name, min(current_price+1, max_bid))

        def disable_auctions_from_past():
            for item in self.items:
                if datetime.now() > parse_string_to_datetime(item['end_auction_time']) and self.username != item['owner_name']:
                    self.entries[item['item_name']]['state'] = 'disabled'
                    self.buttons[item['item_name']]['state'] = 'disabled'
            self.root.after(1000, disable_auctions_from_past)

        def refresh_watched():
            if len(self.grid_fields.keys()) != len(self.items):
                create_grids()
            for item in self.items:
                self.grid_fields[item['item_name']]['current_bid'].configure(text=str(item['current_bid']))
                self.grid_fields[item['item_name']]['current_bid_owner'].configure(text=str(item['current_bid_owner']))
            apply_strategies()
            self.root.after(250, refresh_watched)

        def bid(item_name: str):
            new_price = float(self.entries[item_name].get())
            strategy = self.dropdowns[item_name].get()
            if strategy == 'normal':
                self.bid_item(item_name, new_price)
            elif strategy == "minute before":
                self.minute_before[item_name] = new_price
                self.assigned_server.register_listener(self.username, item_name)
                refresh_all()
            elif strategy == "outbid":
                self.outbid[item_name] = new_price
                self.assigned_server.register_listener(self.username, item_name)
                refresh_all()

        def refresh_all():
            self.items = self.assigned_server.get_items()
            if len(self.grid_fields.keys()) != len(self.items):
                create_grids()
            for item in self.items:
                self.grid_fields[item['item_name']]['current_bid'].configure(text=str(item['current_bid']))
                self.grid_fields[item['item_name']]['current_bid_owner'].configure(text=str(item['current_bid_owner']))

        def create_new_item():
            owner_name = self.username
            item_name = self.new_auction_entries['item_name'].get()
            item_desc = self.new_auction_entries['item_desc'].get()
            current_bid = self.new_auction_entries['minimal_bid'].get()
            end_auction_time = self.new_auction_entries['time_till_end'].get()
            self._logger.info(f'{self.username} place item {item_name} on bid with value {current_bid}')
            self.items = self.assigned_server.place_item_for_bid(owner_name, item_name, item_desc, current_bid, end_auction_time)
            create_grids()

        def create_grids():
            strategies = ["normal", "minute before", "outbid"]
            for label in self.canvas.grid_slaves():
                label.grid_forget()
            self.entries = dict()
            self.buttons = dict()
            self.dropdowns = dict()
            for idx_x, value in enumerate(self.items[0].keys()):
                w = Label(self.canvas, text=value.replace('_', ' '), width=20, height=5)
                w.grid(row=0, column=idx_x)
                w["state"] = DISABLED
            for idx_y, item in enumerate(self.items):
                self.grid_fields[item['item_name']] = dict()
                for idx_x, (field_name, value) in enumerate(item.items()):
                    w = Label(self.canvas, text=value, width=20, height=5)
                    w.grid(row=idx_y + 1, column=idx_x)
                    w["state"] = DISABLED
                    self.grid_fields[item['item_name']][field_name] = w
                if self.username != item['owner_name']:
                    entry = Entry(self.canvas)
                    item_name_copy = str(self.items[idx_y]['item_name'])
                    self.entries[str(item['item_name'])] = entry
                    entry.grid(row=idx_y + 1, column=len(item.values()))
                    button = Button(self.canvas, text='bid', command=lambda name=item_name_copy: bid(name))
                    self.buttons[str(item['item_name'])] = button
                    button.grid(row=idx_y + 1, column=len(item.values())+1)
                    default_variable = StringVar(self.canvas)
                    default_variable.set(strategies[0])
                    dropdown = OptionMenu(self.canvas, default_variable, *strategies)
                    self.dropdowns[str(item['item_name'])] = default_variable
                    dropdown.grid(row=idx_y + 1, column=len(item.values())+2)
            w = Label(self.canvas, text="Create new auction", width=20, height=5)
            w.grid(row=len(self.items)+1, column=0)
            w["state"] = DISABLED
            required_entries = ["item_name", "item_desc", "minimal_bid", "time_till_end"]
            for idx_x, param_name in enumerate(required_entries):
                w = Label(self.canvas, text=param_name.replace('_', ' '), width=20, height=5)
                w.grid(row=len(self.items)+2, column=idx_x)
                w["state"] = DISABLED
            self.new_auction_entries = dict()
            for idx_x, param_name in enumerate(required_entries):
                entry = Entry(self.canvas)
                self.new_auction_entries[param_name] = entry
                entry.grid(row=len(self.items)+3, column=idx_x)
            Button(self.canvas, text='Create auction', command=create_new_item).grid(row=len(self.items)+3, column=len(required_entries))
            Button(self.canvas, text='Refresh', command=refresh_all).grid(row=0, column=len(item.values()))
            w = Label(self.canvas, text="Authors: \n176311\n176062\n183710", width=20, height=5)
            w.grid(row=len(self.items) + 4, column=0)
            w["state"] = DISABLED

        self.root = Tk()
        self.root.title('Auction Client')
        self.items = self.assigned_server.get_items()
        self.grid_fields = dict()
        self.canvas = Canvas(self.root, width=700, height=1200, relief='raised')
        self.canvas.pack()
        frm = Frame(self.canvas)
        frm.grid()
        create_grids()
        refresh_watched()
        disable_auctions_from_past()
        self.root.mainloop()

    def bid_item(self, item_name, new_bid):
        self._logger.info(f'{self.username} bid on {item_name} - value {new_bid}')
        self.assigned_server.bid_on_item(self.username, item_name, new_bid)

    def find_item(self, new_item):
        for idx, item_in_list in enumerate(self.items):
            if item_in_list['item_name'] == new_item:
                return idx

    def update(self, item: bytes = None):
        if item is not None:
            item_obj: Item = pickle.loads(base64.b64decode(item['data']))
            item_index = self.find_item(item_obj.item_name)
            self.items[item_index]['current_bid'] = item_obj.current_bid
            self.items[item_index]['current_bid_owner'] = item_obj.current_bid_owner
            self._logger.info(f'Update {item_obj.item_name} item in client')

    def __str__(self):
        return self.username

    def __hash__(self):
        return hash(str(self.username))

    def __eq__(self, other):
        return hash(str(self.username)) == hash(str(other.username))
