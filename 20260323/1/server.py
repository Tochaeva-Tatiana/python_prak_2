from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import shlex
import socket


class Game:

    def __init__(self):
        self.field = [["-" for j in range(10)] for i in range(10)]
        self.position_x = 0
        self.position_y = 0

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
        jgs     __\\\\'--'//__
                (((""`  `"")))
        EOC
        """))

    def encounter(self, x, y):
        if self.field[y][x] != "-":
            hello, name = self.field[y][x][0], self.field[y][x][1]
            if name == "jgsbat":
                return cowsay(hello, cowfile=self.jgsbat)
            return cowsay(hello, cow=name)
        return ""

    def addmon(self, args):
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
                return f"Added monster {name} to ({x}, {y}) saying {hello}"
            return "Invalid arguments"
        return "Invalid command"

    def move(self, direction):
        if direction == "up":
            self.position_y = (self.position_y + 1) % 10
        elif direction == "down":
            self.position_y = (self.position_y - 1) % 10
        elif direction == "left":
            self.position_x = (self.position_x - 1) % 10
        elif direction == "right":
            self.position_x = (self.position_x + 1) % 10

        answer = self.encounter(self.position_x, self.position_y)
        if answer:
            answer += "\n"
        answer += f"Moved to ({self.position_x}, {self.position_y})"
        return answer

    def attack(self, args):
        data = shlex.split(args)
        if len(data) == 1 or len(data) == 3:
            monster = self.field[self.position_y][self.position_x]

            if monster == "-":
                return "No monster here"
            if monster[1] != data[0]:
                return f"No {data[0]} here"

            if len(data) == 1:
                damage = 10
            else:
                if data[1] != "with":
                    return "Invalid arguments"
                if data[2] == "sword":
                    damage = 10
                elif data[2] == "spear":
                    damage = 15
                elif data[2] == "axe":
                    damage = 20
                else:
                    return "Unknown weapon"

            attack = min(damage, monster[2])
            monster[2] -= attack
            answer = f"Attacked {monster[1]},  damage {attack} hp"

            if monster[2] == 0:
                answer += f"\n{monster[1]} died"
                self.field[self.position_y][self.position_x] = "-"
            else:
                answer += f"\n{monster[1]} now has {monster[2]}"

            return answer
        return "Invalid arguments"

    def process(self, command):
        data = shlex.split(command)
        if not data:
            return ""

        if data[0] == "addmon":
            return self.addmon(command[len("addmon "):])
        if data[0] in ["up", "down", "left", "right"]:
            if len(data) == 1:
                return self.move(data[0])
            return "Invalid arguments"
        if data[0] == "attack":
            return self.attack(command[len("attack "):])

        return "Invalid command"


def main():
    game = Game()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 1337))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        with conn:
            command = conn.recv(4096).decode()
            answer = game.process(command)
            conn.sendall(answer.encode())


if __name__ == "__main__":
    main()