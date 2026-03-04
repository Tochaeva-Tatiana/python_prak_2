from cowsay import cowsay


field = [["-" for j in range(10)] for i in range(10)]
position_x, position_y = 0, 0



def encounter(x: int, y: int):
    if field[y][x] != '-':
        print(cowsay(field[y][x]))


while True:
    com, *args = input().split()
    print(com)
    print(args)
    print(*field, sep="\n")
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
            


