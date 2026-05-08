from cowsay import list_cows
import cmd
import shlex
import socket


class CmdCow(cmd.Cmd):

    def request(self, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 1337))
        sock.sendall(command.encode())
        answer = sock.recv(4096).decode()
        sock.close()
        return answer

    def do_addmon(self, args):
        print(self.request("addmon " + args))

    def do_up(self, args):
        if not args:
            print(self.request("up"))
        else:
            print("Invalid arguments")

    def do_down(self, args):
        if not args:
            print(self.request("down"))
        else:
            print("Invalid arguments")

    def do_left(self, args):
        if not args:
            print(self.request("left"))
        else:
            print("Invalid arguments")

    def do_right(self, args):
        if not args:
            print(self.request("right"))
        else:
            print("Invalid arguments")

    def do_attack(self, args):
        print(self.request("attack " + args))

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

    def cmdloop(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        super().cmdloop()

    def do_EOF(self, args):
        return True


if __name__ == "__main__":
    mud_game = CmdCow()
    mud_game.cmdloop()