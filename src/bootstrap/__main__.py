import asyncio
import logging
import sys
from threading import Thread
from kademlia.network import Server

from ..utils import read_ips


class Bootstrap(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.set_logger()
        self.server = Server()
        self.ip = ip
        self.port = port

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.server.listen(self.port))
        try:
            print(f"[Started] Bootstrap on ip {self.ip} and port {self.port}")
            loop.run_forever()
        except KeyboardInterrupt:
            print(f"[Stopped] Bootstrap on ip {self.ip} and port {self.port}")
        finally:
            loop.stop()

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


def check_args():
    if len(sys.argv) > 2:
        print("Wrong number of argumets."
              "USAGE: python -m src.bootstrap [bootstrap_file]")
        exit()

    bootstrap_file = 'config/default.ini'
    if len(sys.argv) > 1:
        bootstrap_file = sys.argv[1]
    return bootstrap_file


def main(bootstrap_file):
    address_list = read_ips(bootstrap_file)
    for ip, port in address_list:
        Bootstrap(ip, port).start()


if __name__ == '__main__':
    main(check_args())
