from cowsay import cowsay
import sys

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
        print(cowsay(field[y][x]))


while True:
    if fl:
        com, *args = lst[i]
        i += 1
    else:
        com, *args = input().split()
    if com == "addmon":
        
        if (len(args) == 3):
            x, y, hello = args[0], args[1], args[2]
            if (x  in list('1234567890')) and (y in list('1234567890')):
                x = int(x)
                y = int(y)
                field[y][x] = hello
                print(f"Added monster to ({x}, {y}) saying {hello}")
            else:
                print("Invalid arguments")

        else:
            print("Invalid arguments")
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
            