from threading import Thread
import sys


from .control import Controller
from .Peer import Peer

def check_args():
    # Function to check if the arguments are correct

    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Wrong arguments."
              "USAGE: python -m src <ip> <port> [bootstrap_file]")
        exit()

    ip = sys.argv[1]
    bootstrap_file = 'config/default.ini'
    if len(sys.argv) > 3:
        bootstrap_file = sys.argv[3]
    try:
        port = int(sys.argv[2])
    except:
        print("Wrong arguments."
              "USAGE: python -m src <ip> <port> [bootstrap_file]")
        exit()
    return ip, port, bootstrap_file


def main(ip: str, port: int, bootstrap_file: str):

    peer = Peer(ip, port, bootstrap_file)

    # NOTE The listening and bootstrapping are running forever.
    # Putting this before the operation, we are initializing the kademlia server.
    Thread(target=peer.loop.run_forever, daemon=True).start()

    controller = Controller(peer)
    controller.start()


if __name__ == '__main__':
    peer = main(*check_args())
