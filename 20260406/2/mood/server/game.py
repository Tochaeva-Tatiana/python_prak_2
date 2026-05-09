"""Game logic for MOOD server."""

from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import shlex
from mood.common import FIELD_SIZE, WEAPONS
import random


class Game:
    """Game field, players and monsters."""

    def __init__(self):
        """Create empty game field."""
        self.field = [
            ["-" for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)
        ]
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
        """Add player to the game."""
        self.players[username] = [0, 0]

    def del_player(self, username):
        """Delete player from the game."""
        self.players.pop(username, None)

    def encounter(self, x, y):
        """Return monster greeting for current cell."""
        if self.field[y][x] != "-":
            hello, name = self.field[y][x][0], self.field[y][x][1]
            if name == "jgsbat":
                return cowsay(hello, cowfile=self.jgsbat)
            return cowsay(hello, cow=name)
        return ""

    def addmon(self, args, username):
        """Add monster to the field."""
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
                message = (
                    f"{username} added monster {name} "
                    f"to ({x}, {y}) with {hp} hp"
                )
                return "", [message]
            return "Invalid arguments", []
        return "Invalid command", []

    def move(self, direction, username):
        """Move player."""
        position_x, position_y = self.players[username]
        if direction == "up":
            position_y = (position_y + 1) % FIELD_SIZE
        elif direction == "down":
            position_y = (position_y - 1) % FIELD_SIZE
        elif direction == "left":
            position_x = (position_x - 1) % FIELD_SIZE
        elif direction == "right":
            position_x = (position_x + 1) % FIELD_SIZE

        self.players[username] = [position_x, position_y]

        answer = self.encounter(position_x, position_y)
        if answer:
            answer += "\n"
        answer += f"Moved to ({position_x}, {position_y})"
        return answer, []
    
    def wandering_monster(self):
        """Move random monster to a free neighbour cell."""
        monsters = []

        for y in range(10):
            for x in range(10):
                if self.field[y][x] != "-":
                    monsters.append((x, y))

        if not monsters:
            return "", []

        directions = ["up", "down", "left", "right"]

        while True:
            x, y = random.choice(monsters)
            direction = random.choice(directions)

            new_x = x
            new_y = y

            if direction == "up":
                new_y = (new_y + 1) % 10
            elif direction == "down":
                new_y = (new_y - 1) % 10
            elif direction == "left":
                new_x = (new_x - 1) % 10
            elif direction == "right":
                new_x = (new_x + 1) % 10

            if self.field[new_y][new_x] == "-":
                break

        monster = self.field[y][x]
        self.field[new_y][new_x] = monster
        self.field[y][x] = "-"

        encounters = []

        for username in self.players:
            position_x, position_y = self.players[username]
            if position_x == new_x and position_y == new_y:
                encounters.append((username, self.encounter(new_x, new_y)))

        return f"{monster[1]} moved one cell {direction}", encounters

    def attack(self, args, username):
        """Attack monster."""
        data = shlex.split(args)
        if len(data) == 1 or len(data) == 3:
            position_x, position_y = self.players[username]
            monster = self.field[position_y][position_x]

            if monster == "-":
                return "No monster here", []
            if monster[1] != data[0]:
                return f"No {data[0]} here", []

            if len(data) == 1:
                damage = WEAPONS["sword"]
                weapon = "sword"
            else:
                if data[1] != "with":
                    return "Invalid arguments", []
                weapon = data[2]
                if weapon not in WEAPONS:
                    return "Unknown weapon", []
                damage = WEAPONS[weapon]

            attack = min(damage, monster[2])
            monster[2] -= attack
            answer = (
                f"{username} attacked {monster[1]} with {weapon}, "
                f"damage {attack} hp, {monster[2]} hp left"
            )

            if monster[2] == 0:
                answer += f"\n{monster[1]} died"
                self.field[position_y][position_x] = "-"

            return "", [answer]
        return "Invalid arguments", []

    def sayall(self, args, username):
        """Send message to all players."""
        data = shlex.split(args)
        if not data:
            return "Invalid arguments", []

        return "", [f"{username}: {args}"]

    def process(self, command, username):
        """Process player command."""
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
