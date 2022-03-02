import asyncio
from time import ctime, strftime, localtime, time
import ntplib
from .consts import NTP_SERVER, NTP_FREQ, NTP_TRIES
from datetime import date, datetime

offset = 0

def run_in_loop(function, loop):
    return asyncio.run_coroutine_threadsafe(function, loop)


def get_time():
    global offset
    time_now = time() + offset
    return datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')

def sync_time():
    global offset
    ntpclient = ntplib.NTPClient()
    for _ in range(NTP_TRIES):
        try:
            response = ntpclient.request(NTP_SERVER)
            offset = response.offset
            # debug_ntp(response) 
            return 
        except ntplib.NTPException:
            # print("NTP try failed")
            pass


def read_ips(file_path):
    with open(file_path) as file:
        lines = file.readlines()

    def parse_line(line):
        line = line.strip()
        line = line.split()
        line[1] = int(line[1])
        return tuple(line)

    return list(map(parse_line, lines))

def debug_ntp(response):
    print("delay = ", response.delay)
    print("dest_time = ", response.dest_time)
    print("tx_time = ", response.dest_time)
    print("offset = ", response.offset)
    print("delay = ", response.delay)   
    print("dest_time + offset = ", response.dest_time + response.offset)
    print("tx_time + delay/2 = ", response.tx_time + response.delay/2)

    offset = response.offset
    time_t = time()
    print("OLD", time_t)
    print("CORRECT", time_t + offset)
    
# -------------------------------------------------------------------------
# Post utils
# -------------------------------------------------------------------------


def get_post_args(post):
    post_id = post["post_id"]
    user = post["user"]
    date = post["timestamp"]
    body = post["body"]
    return [post_id, user, date, body]


def get_post_fieldnames():
    return ["post_id", "user", "timestamp", "body"]


def post_tuple_to_dict(post):
    positions = get_post_fieldnames()
    return dict(zip(positions, post))


def parse_post(post):
    post_id, post_creator, post_time, post_content = post
    post_time = post_time.split()
    post_day = post_time[0]
    post_hour = post_time[1]
    return post_id, post_creator, post_day, post_hour, post_content

