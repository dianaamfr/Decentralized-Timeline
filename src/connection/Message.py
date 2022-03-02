import json
from time import time, strftime, localtime
from ..utils import get_time


class Message:

    # -------------------------------------------------------------------------
    # Operation specific messages
    # -------------------------------------------------------------------------

    @staticmethod
    def sync_posts(user, last_post_id, username):
        return Message.new(user, "sync_posts", {
            "last_post_id": last_post_id,
            "username": username,
        })

    @staticmethod
    def sync_with_online_user(user, last_post_id):
        return Message.new(user, "sync_with_online_user", {
            "last_post_id": last_post_id
        })

    @staticmethod
    def follow(user):
        return Message.new(user, "follow", {})

    @staticmethod
    def unfollow(user):
        return Message.new(user, "unfollow", {})

    @staticmethod
    def post(post_id, user, body, timestamp=None):
        args = {
            "post_id": post_id,
            "body": body,
        }

        if timestamp is not None:
            args["timestamp"] = timestamp
        return Message.new(user, "post", args)

    @staticmethod 
    def online(username): 
        return Message.new(username, "online")

    # -------------------------------------------------------------------------
    # Creation and parsing
    # -------------------------------------------------------------------------

    @staticmethod
    def new(user, operation, args={}):
        args["user"] = user 
        args["operation"] = operation
        if "timestamp" not in args:
            args["timestamp"] = str(get_time())
        return json.dumps(args)

    @staticmethod
    def parse_json(line):
        line = line.strip()
        line = line.decode()
        return json.loads(line)

    @staticmethod
    def get_operation(message):
        return message["operation"]
