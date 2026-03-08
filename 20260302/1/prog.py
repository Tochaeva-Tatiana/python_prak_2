from cowsay import cowsay, list_cows, read_dot_cow
import sys
from io import StringIO

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

field = [["-" for j in range(10)] for i in range(10)]
position_x, position_y = 0, 0

fl = False
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        lst = f.readlines()
        fl = True
        i = 0



def encounter(x: int, y: int):
    if field[y][x] != '-':
        hello, name = field[y][x][0], field[y][x][1]
        if name == 'jgsbat':
        # Используем cowfile
            print(cowsay(hello, cowfile=jgsbat))
        else:
        # Используем имя (для стандартных коров)
            print(cowsay(hello, cow=name))


print("<<< Welcome to Python-MUD 0.1 >>>")
while True:
    if fl:
        com, *args = lst[i]
        i += 1
    else:
        com, *args = input().split()
    if com == "addmon":
        
        if (len(args) == 4):
            name, x, y, hello = args[0], args[1], args[2], args[3]
            if (x  in list('1234567890')) and (y in list('1234567890')) and (name in (list_cows() + ['jgsbat'])):
                x = int(x)
                y = int(y)
                field[y][x] = [hello, name]
                print(f"Added monster {name} to ({x}, {y}) saying {hello}")
            else:
                print("Invalid arguments")
                print(1)

        else:
            print("Invalid arguments")
            print(2)
    elif com in ["up", "down", "left", "right"]:
        if len(args) == 0:
            if com == "up":
                position_y = (position_y - 1) % 10
            elif com == "down":
                position_y = (position_y + 1) % 10
            elif com == "left":
                position_x = (position_x - 1) % 10
            else:
                position_x = (position_x + 1) % 10
            print(f"Moved to ({position_x}, {position_y})")
            encounter(position_x, position_y)
        else:
            print("Invalid arguments")
    else:
        print("Invalid command")
