from __future__ import annotations

import logging
import asyncio

from kademlia.network import Server

from .KademliaInfo import KademliaInfo
from .connection import Sender
from .utils import read_ips


class Node:
    def __init__(self, ip, port, bootstrap_file):
        self.set_logger()
        self.server = Server()
        self.ip = ip
        self.port = port

        # NOTE When a function reaches an io operation, it will switch between the functions called with this loop.
        # The program has only one event loop.
        self.loop = asyncio.get_event_loop()

        # Read Bootstrap nodes from file
        self.b_nodes = read_ips(bootstrap_file)

        self.loop.run_until_complete(self.server.listen(self.port))
        self.loop.run_until_complete(self.server.bootstrap(self.b_nodes))

    # --------------------------------------------------------------------------
    # Logger
    # --------------------------------------------------------------------------

    def set_logger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)

    # --------------------------------------------------------------------------
    # Communication with other nodes
    # --------------------------------------------------------------------------

    def send_message(self, destiny_ip: str, destiny_port: int, message):
        asyncio.run_coroutine_threadsafe(Sender.send_message(
            destiny_ip, destiny_port, message), loop=self.loop)

    # --------------------------------------------------------------------------
    # Kademlia
    # --------------------------------------------------------------------------

    async def set_kademlia_info(self, key: str, kademlia_info) -> None:
        """
        Set's a value for the key self.username in the network.
        The value contains the peer properties.
        """
        await self.server.set(key, kademlia_info.serialize)

    async def get_kademlia_info(self, key: str) -> KademliaInfo | None:
        """
        Get the value associated with the given username from the network.
        """
        info = await self.server.get(key)
        if info is None:
            return None
        return KademliaInfo.deserialize(info)
