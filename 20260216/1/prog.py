import sys
from pathlib import Path
import zlib

while True:
    data_str = input().split()
    if data_str == ['end']:
        break
    elif len(data_str) == 1:
        data_gen = Path(data_str[0]).glob('.git/refs/heads/*')
        print(*[str(data).split('/')[-1] for data in data_gen], sep='\n')

    elif len(data_str) == 3:
        branch = Path(data_str[1] + '.git/refs/heads/' + data_str[2])
        if data_str[0] == 'commit':
            data_hesh = str(branch.read_bytes().decode('utf-8'))
            obj_commit = Path(data_str[1] + '.git/objects/' + data_hesh[:2] + '/'+ data_hesh[2:-1])
            data = zlib.decompress(obj_commit.read_bytes()).partition(b'\x00')
            print(data[-1].decode('utf-8'))

