from threading import Thread
from .utils import sync_time
from .consts import NTP_FREQ

class EventThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stop = event

    def run(self):
        while not self.stop.wait(NTP_FREQ):
            sync_time()