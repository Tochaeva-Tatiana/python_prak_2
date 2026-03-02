import shlex

while True:
    s = shlex.split(input())
    print(s[0], len(s) - 1, s[1:])
    s = shlex.join(s)
    print(s)
