from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import shlex
import socket
import asyncio


class Game:

    def __init__(self):
        self.field = [["-" for j in range(10)] for i in range(10)]
        self.players = {}


        self.jgsbat = read_dot_cow(StringIO(r"""
        $the_cow = <<EOC;
                $thoughts
                $thoughts
             ,_                    _,
             ) '-._  ,_    _,  _.-' (
            )  _.-'.|\\\\--//|.'-._  (
              )'   .'\/o\/o\/'.   `(
               ) .' . \====/ . '. (
                )  / <<    >> \  (
                '-._/``  ``\_.-'
        jgs      __\\\\'--'//__
                 (((""`  `"")))
        EOC
        """))
    
    def add_player(self, username):
        self.players[username] = [0, 0]

    def del_player(self, username):
        self.players.pop(username, None)

    def encounter(self, x, y):
        if self.field[y][x] != "-":
            hello, name = self.field[y][x][0], self.field[y][x][1]
            if name == "jgsbat":
                return cowsay(hello, cowfile=self.jgsbat)
            return cowsay(hello, cow=name)
        return ""

    def addmon(self, args, username):
        data = shlex.split(args)
        if len(data) == 8:
            name = data[0]
            hp = ""
            hello = ""
            x = ""
            y = ""
            j = 1

            while j < len(data):
                if data[j] == "hp":
                    hp = data[j + 1]
                elif data[j] == "hello":
                    hello = data[j + 1]
                elif data[j] == "coords":
                    x, y = data[j + 1], data[j + 2]
                    j += 1
                j += 2

            if (
                hp.isdigit()
                and x in list("1234567890")
                and y in list("1234567890")
                and name in (list_cows() + ["jgsbat"])
            ):
                x = int(x)
                y = int(y)
                hp = int(hp)
                self.field[y][x] = [hello, name, hp]
                return "", [f"{username} added monster {name} to ({x}, {y}) with {hp} hp"]
            return "Invalid arguments", []
        return "Invalid command", []

    def move(self, direction, username):
        position_x, position_y = self.players[username]
        if direction == "up":
            position_y = (position_y + 1) % 10
        elif direction == "down":
            position_y = (position_y - 1) % 10
        elif direction == "left":
            position_x = (position_x - 1) % 10
        elif direction == "right":
            position_x = (position_x + 1) % 10
        
        self.players[username] = [position_x, position_y]

        answer = self.encounter(position_x, position_y)
        if answer:
            answer += "\n"
        answer += f"Moved to ({position_x}, {position_y})"
        return answer, []

    def attack(self, args, username):
        data = shlex.split(args)
        if len(data) == 1 or len(data) == 3:
            position_x, position_y = self.players[username]
            monster = self.field[position_y][position_x]

            if monster == "-":
                return "No monster here", []
            if monster[1] != data[0]:
                return f"No {data[0]} here", []

            if len(data) == 1:
                damage = 10
                weapon = "sword" 
            else:
                if data[1] != "with":
                    return "Invalid arguments", []
                weapon = data[2]
                if weapon == "sword":
                    damage = 10
                elif weapon == "spear":
                    damage = 15
                elif weapon == "axe":
                    damage = 20
                else:
                    return "Unknown weapon", []

            attack = min(damage, monster[2])
            monster[2] -= attack
            answer =  f"{username} attacked {monster[1]} with {weapon}, damage {attack} hp, {monster[2]} hp left"

            if monster[2] == 0:
                answer += f"\n{monster[1]} died"
                self.field[position_y][position_x] = "-"

            return [], [answer]
        return "Invalid arguments", []
    
    def sayall(self, args, username):
        data = shlex.split(args)
        if not data:
            return "Invalid arguments", []

        return "", [f"{username}: {args}"]

    def process(self, command, username):
        data = shlex.split(command)
        if not data:
            return "", []

        if data[0] == "addmon":
            return self.addmon(command[len("addmon "):], username)
        if data[0] in ["up", "down", "left", "right"]:
            if len(data) == 1:
                return self.move(data[0], username)
            return "Invalid arguments", []
        if data[0] == "attack":
            return self.attack(command[len("attack "):], username)
        if data[0] == "sayall":
            return self.sayall(command[len("sayall "):], username)

        return "Invalid command", []



class Server:

    def __init__(self):
        self.game = Game()
        self.clients = {}

    async def send_to(self, username, message):
        if not message:
            return

        writer = self.clients.get(username)
        if writer is None:
            return

        writer.write((message + "\n").encode())
        await writer.drain()

    async def broadcast(self, message):
        if not message:
            return

        for username in list(self.clients):
            await self.send_to(username, message)

    async def handle_client(self, reader, writer):
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
        server = await asyncio.start_server(
            self.handle_client,
            "localhost",
            1337
        )

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(Server().run())