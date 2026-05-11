"""MOOD server."""

import asyncio

from mood.common import HOST, PORT
from mood.server.game import Game
import gettext
from pathlib import Path

LOCALEDIR = Path(__file__).parent / "po"

class Server:
    """MOOD server."""

    def __init__(self):
        """Create server."""
        self.game = Game()
        self.clients = {}
        self.moving_monsters = True
        self.locales = {}

    async def send_to(self, username, message, *args):
        """Send message to one player."""
        if not message:
            return

        writer = self.clients.get(username)
        if writer is None:
            return
        
        translation = self.translation(username)
        
        if isinstance(message, tuple) and message[0] == "attack":
            _, player, monster, weapon, damage, hp_left = message

            damage_text = translation.ngettext(
                "{} hp",
                "{} hp",
                damage,
            ).format(damage)

            hp_left_text = translation.ngettext(
                "{} hp",
                "{} hp",
                hp_left,
            ).format(hp_left)

            message = translation.gettext(
                "{} attacked {} with {}, damage {}, {} left"
            ).format(player, monster, weapon, damage_text, hp_left_text)

        elif isinstance(message, tuple) and message[0] == "ngettext":
            singular = message[1]
            plural = message[2]
            number = message[3]
            format_args = message[4]

            message = translation.ngettext(
                singular,
                plural,
                number,
            ).format(*format_args)

        elif isinstance(message, tuple):
            args = message[1:]
            message = message[0]
            message = translation.gettext(message).format(*args)

        elif args:
            message = translation.gettext(message).format(*args)

        else:
            message = translation.gettext(message)

        writer.write((message + "\n").encode())
        await writer.drain()

    async def broadcast(self, message, *args):
        """Send message to all players."""
        if not message:
            return

        for username in list(self.clients):
            await self.send_to(username, message, *args)

    async def movemonsters(self, username, args):
        """Turn wandering monsters on or off."""
        if args == "on":
            self.moving_monsters = True
            await self.send_to(username, "Moving monsters: on")
        elif args == "off":
            self.moving_monsters = False
            await self.send_to(username, "Moving monsters: off")
        else:
            await self.send_to(username, "Invalid arguments")
    
    async def set_locale(self, username, args):
        """Set client locale."""
        self.locales[username] = args
        await self.send_to(username, "Set up locale: {}", args)

    def translation(self, username):
        """Return translation for client."""
        locale = self.locales.get(username)

        if locale == "ru_RU.UTF8":
            return gettext.translation(
                "mood_server",
                localedir=LOCALEDIR,
                languages=["ru_RU"],
                fallback=True,
            )

        return gettext.NullTranslations()

    async def wandering_monsters(self):
        """Move monsters every 30 seconds."""
        while True:
            await asyncio.sleep(30)

            if not self.moving_monsters:
                continue

            message, encounters = self.game.wandering_monster()

            await self.broadcast(message)

            for username, encounter in encounters:
                await self.send_to(username, encounter)

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

            await self.broadcast("{} entered MUD", username)

            while not reader.at_eof():
                command = (await reader.readline()).decode().strip()

                if not command:
                    continue

                if command == "quit":
                    break

                if command.startswith("movemonsters "):
                    await self.movemonsters(
                        username,
                        command[len("movemonsters "):],
                    )
                    continue

                if command.startswith("locale "):
                    await self.set_locale(
                        username,
                        command[len("locale "):],
                    )
                    continue

                answer, messages = self.game.process(command, username)

                await self.send_to(username, answer)

                for message in messages:
                    await self.broadcast(message)

        finally:
            if username in self.clients:
                self.clients.pop(username)
                self.locales.pop(username, None)
                self.game.del_player(username)
                await self.broadcast("{} left MUD", username)

            writer.close()
            await writer.wait_closed()

    async def run(self):
        """Run server."""
        server = await asyncio.start_server(
            self.handle_client,
            HOST,
            PORT,
        )

        asyncio.create_task(self.wandering_monsters())

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(Server().run())
