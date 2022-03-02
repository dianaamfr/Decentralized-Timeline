import socket
import asyncio


class Sender:
    @staticmethod
    async def send_message(ip, port, message):
        try:
            _, writer = await asyncio.open_connection(ip, port) 
            writer.write(message.encode())
            writer.write_eof()
            await writer.drain()
            return True
        except Exception as e:
            return False