from cowsay import list_cows
import cmd
import shlex
import socket
import asyncio
import sys


class CmdCow(cmd.Cmd):

    prompt = "(MUD) "

    def __init__(self, username, reader, writer):
        super().__init__()
        self.username = username
        self.reader = reader
        self.writer = writer

    def request(self, command):
        self.writer.write((command + "\n").encode())

    def do_addmon(self, args):
        self.request("addmon " + args)

    def do_up(self, args):
        if not args:
            self.request("up")
        else:
            print("Invalid arguments")

    def do_down(self, args):
        if not args:
            self.request("down")
        else:
            print("Invalid arguments")

    def do_left(self, args):
        if not args:
            self.request("left")
        else:
            print("Invalid arguments")

    def do_right(self, args):
        if not args:
            self.request("right")
        else:
            print("Invalid arguments")

    def do_attack(self, args):
        self.request("attack " + args)

    def complete_attack(self, text, line, begidx, endidx):
        data = shlex.split(line)
        lst_monsters = list_cows() + ["jgsbat"]
        weapons = ["sword", "spear", "axe"]

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
        self.request("quit")
        return True

    def do_EOF(self, args):
        print()
        return self.do_quit(args)


async def read_server(reader):
    while True:
        answer = await reader.readline()

        if not answer:
            print("\nDisconnected from server")
            break

        print(answer.decode().rstrip(), flush=True)

async def read_user(cmdline):
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


async def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py username")
        return

    username = sys.argv[1]

    reader, writer = await asyncio.open_connection("localhost", 1337)

    writer.write((username + "\n").encode())
    await writer.drain()

    answer = (await reader.readline()).decode().strip()

    if answer != "OK":
        print(answer)
        writer.close()
        await writer.wait_closed()
        return

    print("<<< Welcome to Python-MUD 0.1 >>>")

    cmdline = CmdCow(username, reader, writer)

    await asyncio.gather(
        read_server(reader),
        read_user(cmdline)
    )


if __name__ == "__main__":
    asyncio.run(main())