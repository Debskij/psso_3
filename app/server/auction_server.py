from abc import ABC, abstractmethod

from app.client.auction_listener import AuctionListener


class AuctionServer(ABC):
    @abstractmethod
    def place_item_for_bid(self, owner_name: str, item_name: str, item_desc: str,
                           start_bid: float, auction_time: int) -> None:
        """
        Puts a new item up for auction by the owner with name owner_name.
        If an item by that name already is up for auction in the server,
        an Exception is thrown. The item will be available for auction for
        the number of seconds given by the auction_time argument.

        :param owner_name: owner of item
        :param item_name: identifies the new item to be auctioned
        :param item_desc: item description
        :param start_bid: starting minimum bid value
        :param auction_time: number of seconds
        """
        raise NotImplementedError

    @abstractmethod
    def bid_on_item(self, bidder_username: str, item_name: str, bid: float) -> bool:
        """
        The bidder with name bidder_username makes a new
        bid on the item specified by the item_name argument.
        For the bid to be accepted it must be higher than the
        current bid on the specified item, else a Exception is thrown.

        :param bidder_username: name of bidder
        :param item_name: name of item on the bid
        :param bid: new value for item
        :return: ...
        """
        raise NotImplementedError

    @abstractmethod
    def get_items(self) -> list:
        """
        :return: an list of items available for auction. Each
        Item object consists of the owner's name, item name,
        item description, current bid, current bidder's name
        and time remaining on the auction period for the item.
        """
        raise NotImplementedError

    @abstractmethod
    def register_listener(al: AuctionListener, item_name: str):
        """
        Registers a listener with the auction server for changes in
        the item specified by the item_name argument. Whenever the
        current bid on the specified item changes (or its auction period expires),
        the AuctionListener is notified via its update() method.
        Note that the IAuctionListener object is a remote object!

        :param item_name:
        :return:
        """
        raise NotImplementedError
