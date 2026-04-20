import socket
import sys

def sqroots(coeffs : str) -> str:
    a, b, c = coeffs.split()
    a, b, c = int(a), int(b), int(c) 
    d = b**2 - 4*a*c
    if d < 0:
        return ''
    elif d == 0:
        return str(-b / 2*a)
    else:
        return str((-b + d**(1/2)) / (2*a)) + ' ' + str((-b - d**(1/2)) / (2*a))
    

def sqrootnet(coeffs: str, s: socket.socket) -> str:
    s.sendall((coeffs + "\n").encode())
    return s.recv(128).decode().strip()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 1337))
        s.sendall(sys.argv[1].encode() + b'\n')
        print(s.recv(1024).rstrip().decode())
