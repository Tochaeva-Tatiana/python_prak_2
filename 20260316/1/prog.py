from cowsay import cowsay, list_cows, read_dot_cow
import sys
from io import StringIO
import cmd
import shlex


class cmd_cow(cmd.Cmd):

    field = [["-" for j in range(10)] for i in range(10)]
    position_x, position_y = 0, 0
    file_com = None
    i = 0

    jgsbat = read_dot_cow(StringIO(r"""
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

    def __init__(self):
        super().__init__()
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                self.file_com = [shlex.split(line.strip()) for line in f if line.strip()]

    def encounter(self, x: int, y: int):
        if self.field[y][x] != '-':
            hello, name = self.field[y][x][0], self.field[y][x][1]
            if name == 'jgsbat':
                print(cowsay(hello, cowfile=self.jgsbat))
            else:
                print(cowsay(hello, cow=name))

    def do_addmon(self, args):
        data = shlex.split(args)
        if (len(data) == 8):
            name = data[0]
            j = 1
            while j < len(data):
                if data[j] == 'hp':
                    hp = data[j+1]
                elif data[j] == 'hello':
                    hello = data[j+1]
                elif data[j] == 'coords':
                    x, y = data[j+1], data[j+2]
                    j += 1
                j += 2
            if (hp.isdigit()) and (x in list("1234567890")) and (y in list("1234567890")) \
                and (name in (list_cows() + ['jgsbat'])):
                x = int(x)
                y = int(y)
                hp = int(hp)
                self.field[y][x] = [hello, name, hp]
                print(f"Added monster {name} to ({x}, {y}) saying {hello}")
            else:
                print("Invalid arguments")
        else:
            print("Invalid command")


    def do_up(self, args):
        if not args:
            
            self.position_y = (self.position_y + 1) % 10
            self.encounter(self.position_x, self.position_y)
            print(f"Moved to ({self.position_x}, {self.position_y})")
        else:
            print("Invalid arguments")
  

    def do_down(self, args):
        if not args:
            self.position_y = (self.position_y - 1) % 10
            self.encounter(self.position_x, self.position_y)
            print(f"Moved to ({self.position_x}, {self.position_y})")
        else:
            print("Invalid arguments")


    def do_left(self, args):
        if not args:
            self.position_x = (self.position_x - 1) % 10
            self.encounter(self.position_x, self.position_y)
            print(f"Moved to ({self.position_x}, {self.position_y})")
        else:
            print("Invalid arguments")
                

    def do_right(self, args):
        if not args:
            self.position_x = (self.position_x + 1) % 10
            self.encounter(self.position_x, self.position_y)
            print(f"Moved to ({self.position_x}, {self.position_y})")
        else:
            print("Invalid arguments")

    def do_attack(self, args):
        data = shlex.split(args)
        if len(data) == 3 or len(data) == 1:
            monster = self.field[self.position_y][self.position_x]
            if monster == '-':
                print("No monster here")
                return 
            elif monster[1] != data[0]:
                print(f"No {data[0]} here")
                return
            if len(data) == 1:
                damage = 10
            else:
                if data[1] == 'with':
                    if data[2] == 'sword':
                        damage = 10
                    elif data[2] ==  'spear':
                        damage = 15
                    elif data[2] == 'axe':
                        damage = 20
                    else:
                        print("Unknown weapon")
                        return
                else:
                    print("Invalid arguments")
                    return
            attack = min(damage, monster[2])
            monster[2] -= attack
            print(f"Attacked {monster[1]},  damage {attack} hp")
            if monster[2] == 0:
                print(f"{monster[1]} died")
                self.field[self.position_y][self.position_x] = '-'
            else:
                print(f"{monster[1]} now has {monster[2]}")
        else:
            print("Invalid arguments")

    def complete_attack(self, text, line, begidx, endidx):
        data = shlex.split(line)
        lst_monsters = list_cows() + ['jgsbat']
        weapons = ['sword', 'spear', 'axe']
        if len(data) == 2:
            return [m for m in lst_monsters if m.startswith(text)]
        elif len(data) == 3:
            if 'with'.startswith(text):
                return ['with']
        elif len(data) == 4 and data[2] != 'with':
            if 'with'.startswith(data[1]):
                return ['with']
        elif len(data) >= 4 and data[2] == 'with':
            return [w for w in weapons if w.startswith(text)]
        return []



    def cmdloop(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        if self.file_com:
            while self.i < len(self.file_com):
                command_parts = self.file_com[self.i]
                self.i += 1
                command_str = " ".join(command_parts)
                stop = self.onecmd(command_str)
                if stop:
                    return
        else:
            super().cmdloop()

    def do_EOF(self, args):
        return True



if __name__ == '__main__':
    mud_game = cmd_cow()
    mud_game.cmdloop()
