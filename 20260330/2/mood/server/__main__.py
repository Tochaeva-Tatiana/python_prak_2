"""MOOD server."""

import asyncio

from mood.common import HOST, PORT
from mood.server.game import Game


class Server:
    """MOOD server."""

    def __init__(self):
        """Create server."""
        self.game = Game()
        self.clients = {}

    async def send_to(self, username, message):
        """Send message to one player."""
        if not message:
            return

        writer = self.clients.get(username)
        if writer is None:
            return

        writer.write((message + "\n").encode())
        await writer.drain()

    async def broadcast(self, message):
        """Send message to all players."""
        if not message:
            return

        for username in list(self.clients):
            await self.send_to(username, message)

    async def handle_client(self, reader, writer):
        """Handle one client."""
        username = ""

        try:
            username = (await reader.readline()).decode().strip()

            if not username or " " in username or username in self.clients:
                writer.write(b"ERROR bad or busy username\n")
                await writer.drain()
                return

            self.clients[username] = writer
            self.game.add_player(username)

            writer.write(b"OK\n")
            await writer.drain()

            await self.broadcast(f"{username} entered MUD")

            while not reader.at_eof():
                command = (await reader.readline()).decode().strip()

                if not command:
                    continue

                if command == "quit":
                    break

                answer, messages = self.game.process(command, username)

                await self.send_to(username, answer)

                for message in messages:
                    await self.broadcast(message)

        finally:
            if username in self.clients:
                self.clients.pop(username)
                self.game.del_player(username)
                await self.broadcast(f"{username} left MUD")

            writer.close()
            await writer.wait_closed()

    async def run(self):
        """Run server."""
        server = await asyncio.start_server(
            self.handle_client,
            HOST,
            PORT,
        )

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(Server().run())
