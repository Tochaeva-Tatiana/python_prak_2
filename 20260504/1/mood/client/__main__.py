"""MOOD client."""

from cowsay import list_cows
import asyncio
import cmd
import shlex
import sys
from mood.common import HOST, PORT, WEAPONS
import webbrowser
from pathlib import Path


class CmdCow(cmd.Cmd):
    """MOOD command line."""

    prompt = "(MUD) "

    def __init__(self, username, reader, writer):
        """Create command line."""
        super().__init__()
        self.username = username
        self.reader = reader
        self.writer = writer

    def do_documentation(self, args):
        """Open generated documentation."""
        doc_path = Path(__file__).parent.parent / "documentation" / "index.html"
        webbrowser.open(doc_path.resolve().as_uri())

    def request(self, command):
        """Send command to server."""
        self.writer.write((command + "\n").encode())

    def do_addmon(self, args):
        """Add monster."""
        self.request("addmon " + args)

    def do_up(self, args):
        """Move up."""
        if not args:
            self.request("up")
        else:
            print("Invalid arguments")

    def do_down(self, args):
        """Move down."""
        if not args:
            self.request("down")
        else:
            print("Invalid arguments")

    def do_left(self, args):
        """Move left."""
        if not args:
            self.request("left")
        else:
            print("Invalid arguments")

    def do_right(self, args):
        """Move right."""
        if not args:
            self.request("right")
        else:
            print("Invalid arguments")

    def do_sayall(self, args):
        """Send message to all players."""
        self.request("sayall " + args)

    def do_movemonsters(self, args):
        """Turn wandering monsters on or off."""
        self.request("movemonsters " + args)

    def do_locale(self, args):
        """Set locale."""
        self.request("locale " + args)

    def do_attack(self, args):
        """Attack monster."""
        self.request("attack " + args)

    def complete_attack(self, text, line, begidx, endidx):
        """Complete attack command."""
        data = shlex.split(line)
        lst_monsters = list_cows() + ["jgsbat"]
        weapons = list(WEAPONS)

        if len(data) == 2:
            return [m for m in lst_monsters if m.startswith(text)]
        if len(data) == 3:
            if "with".startswith(text):
                return ["with"]
        if len(data) == 4 and data[2] != "with":
            if "with".startswith(data[1]):
                return ["with"]
        if len(data) >= 4 and data[2] == "with":
            return [w for w in weapons if w.startswith(text)]
        return []

    def do_quit(self, args):
        """Quit game."""
        self.request("quit")
        return True

    def do_EOF(self, args):
        """Quit game by EOF."""
        print()
        return self.do_quit(args)


async def read_server(reader):
    """Read messages from server."""
    while True:
        answer = await reader.readline()

        if not answer:
            print("\nDisconnected from server")
            break

        print(answer.decode().rstrip(), flush=True)


async def read_user(cmdline, filename=None):
    """Read user commands."""
    if filename is None:
        loop = asyncio.get_event_loop()

        while True:
            line = await loop.run_in_executor(None, input)

            if line == "EOF":
                line = "quit"

            stop = cmdline.onecmd(line)

            await cmdline.writer.drain()

            if stop:
                cmdline.writer.close()
                await cmdline.writer.wait_closed()
                break
    else:
        with open(filename, encoding="utf-8") as file:
            cmdline.prompt = ""
            cmdline.use_rawinput = False

            for line in file:
                line = line.strip()

                if not line:
                    continue

                stop = cmdline.onecmd(line)

                await cmdline.writer.drain()

                if stop:
                    break

                await asyncio.sleep(1)

        cmdline.writer.close()
        await cmdline.writer.wait_closed()


async def main():
    """Run client."""
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Usage: python -m mood.client username [--file filename]")
        return

    username = sys.argv[1]
    filename = None
    if len(sys.argv) == 4:
        if sys.argv[2] != "--file":
            print("Usage: python -m mood.client username [--file filename]")
            return
        filename = sys.argv[3]

    reader, writer = await asyncio.open_connection(HOST, PORT)

    writer.write((username + "\n").encode())
    await writer.drain()

    answer = (await reader.readline()).decode().strip()

    if answer != "OK":
        print(answer)
        writer.close()
        await writer.wait_closed()
        return

    print("<<< Welcome to Python-MOOD 0.1 >>>")

    cmdline = CmdCow(username, reader, writer)

    await asyncio.gather(
        read_server(reader),
        read_user(cmdline, filename),
    )

def main_sync():
    """Run client."""
    asyncio.run(main())

if __name__ == "__main__":
    main_sync()
