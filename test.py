import Pyro4
import sys

from app.server.server import Server
from app.client.client import Client

Pyro4.Daemon.serveSimple(
    {
        Client: "default.client"
    },
    ns = False 
)

