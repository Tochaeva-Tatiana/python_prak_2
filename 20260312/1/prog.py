from cowsay import cowsay, list_cows, read_dot_cow
import sys
from io import StringIO
import cmd
import shlex


class cmd_cow(cmd.Cmd):

    field = [["-" for j in range(10)] for i in range(10)]
    position_x, position_y = 0, 0
    file = None

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
                self.file = f.readlines()

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
            if (hp.isdigit()) and (x.isdigit()) and (y.isdigit()) and (name in (list_cows() + ['jgsbat'])):
                x = int(x)
                y = int(y)
                hp = int(hp)
                self.field[y][x] = [hello, name, hp]
                print(f"Added monster {name} to ({x}, {y}) saying {hello}")
            else:
                print("Invalid arguments")


    def do_up(self, args):
        if not args:
            self.position_y = (self.position_y + 1) % 10
            self.encounter(self.position_x, self.position_y)
  

    def do_down(self, args):
        if not args:
            self.position_y = (self.position_y - 1) % 10
            self.encounter(self.position_x, self.position_y)


    def do_left(self, args):
        if not args:
            self.position_x = (self.position_x - 1) % 10
            self.encounter(self.position_x, self.position_y)
                

    def do_right(self, args):
        if not args:
            self.position_x = (self.position_x + 1) % 10
            self.encounter(self.position_x, self.position_y)



if __name__ == '__main__':
    mud_game = cmd_cow()
    mud_game.cmdloop()


# print("<<< Welcome to Python-MUD 0.1 >>>")
# while True:
#     if fl:
#         com, *args = shlex.split(lst[i])
#         i += 1
#     else:
#         com, *args = shlex.split(input())
    
#     if com == "addmon":
#         if (len(args) == 8):
#             name = args[0]
#             j = 1
#             while j < len(args):
#                 if args[j] == 'hp':
#                     hp = args[j+1]
#                 elif args[j] == 'hello':
#                     hello = args[j+1]
#                 elif args[j] == 'coords':
#                     x, y = args[j+1], args[j+2]
#                     j += 1
#                 j += 2
#             if (hp.isdigit()) and (x  in list('1234567890')) and (y in list('1234567890')) and (name in (list_cows() + ['jgsbat'])):
#                 x = int(x)
#                 y = int(y)
#                 hp = int(hp)
#                 field[y][x] = [hello, name, hp]
#                 print(f"Added monster {name} to ({x}, {y}) saying {hello}")
#             else:
#                 print("Invalid arguments")

#         else:
#             print("Invalid arguments")
#     elif com in ["up", "down", "left", "right"]:
#         if len(args) == 0:
#             if com == "up":
#                 position_y = (position_y + 1) % 10
#             elif com == "down":
#                 position_y = (position_y - 1) % 10
#             elif com == "left":
#                 position_x = (position_x - 1) % 10
#             else:
#                 position_x = (position_x + 1) % 10
#             print(f"Moved to ({position_x}, {position_y})")
#             encounter(position_x, position_y)
#         else:
#             print("Invalid arguments")
#     else:
#         print("Invalid command")

