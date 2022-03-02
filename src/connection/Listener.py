import asyncio
import json
from threading import Thread
from ..database import Database
from .Message import Message
from ..utils import run_in_loop

BUFFER = 1024


class Listener(Thread):
    def __init__(self, ip, port, peer):
        super().__init__()
        self.ip = ip
        self.port = port
        self.peer = peer

    # -------------------------------------------------------------------------
    # Request handlings
    # -------------------------------------------------------------------------

    async def handle_request(self, reader, writer):
        line = await reader.read(-1)

        if line:
            message = Message.parse_json(line)

            operation = Message.get_operation(message)
            if operation == "follow":
                self.handle_follower(message)
            elif operation == "unfollow":
                self.handle_unfollow(message)
            elif operation == "post":
                self.handle_post(message)
            elif operation == "sync_posts":
                await self.handle_sync_posts(message, writer)
            elif operation == "sync_with_online_user":
                await self.handle_sync_with_online_user(message)
            elif operation == "online":
                await self.handle_online(message)
            else:
                print("Invalid operation")

        writer.close()

    def handle_follower(self, message) -> None:
        run_in_loop(self.peer.add_follower(message["user"]), self.peer.loop)
        run_in_loop(self.peer.send_all_previous_posts(message["user"]),
                    self.peer.loop)

    def handle_unfollow(self, message) -> None:
        run_in_loop(self.peer.remove_follower(
            message["user"]), self.peer.loop)

    def handle_post(self, message) -> None:
        """
        Handles the reception of a post from a user that this peer is following.
        """
        if message["user"] in self.peer.info.following:
            self.peer.database.insert_post(message)

    async def handle_sync_posts(self, message, writer) -> None:
        """
        When the user is back online it requests the posts it lost while offline
        """
        posts = json.dumps(self.peer.database.get_posts_after(
            message["username"],
            message["last_post_id"]))
            
        if message["username"] == self.peer.username:
            await self.peer.update_kademlia_last_post()

        writer.write(posts.encode())
        writer.write_eof()
        await writer.drain()
    

    async def handle_online(self, message):
        """
        Request missing posts to a user that we follow and that just came back online
        """
        try: 
            online_user = message["user"]
            last_post_id = self.peer.database.get_last_post(online_user)

            sync_message = Message.sync_with_online_user(
                self.peer.username,
                last_post_id)

            online_user_info = await self.peer.get_kademlia_info(online_user)
            # Request the missnig posts, when the owner is back online.
            if online_user_info is not None:
                self.peer.send_message(online_user_info.ip, online_user_info.port, sync_message)
        except Exception as e: 
            print(e)

    async def handle_sync_with_online_user(self, message) -> None:
        last_post_id = message["last_post_id"]
        user_info = await self.peer.get_kademlia_info(message["user"])

        run_in_loop(self.peer.resend_missing_posts(user_info.ip, user_info.port, last_post_id), self.peer.loop)

    # -------------------------------------------------------------------------
    # Running listener functions
    # -------------------------------------------------------------------------

    async def serve(self):
        self.server = await asyncio.start_server(
            self.handle_request,
            self.ip,
            self.port
        )
        await self.server.serve_forever()

    def run(self):
        listener_loop = asyncio.new_event_loop()
        listener_loop.run_until_complete(self.serve())
