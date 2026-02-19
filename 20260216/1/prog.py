import sys
from pathlib import Path
import zlib

while True:
    data_str = input().split()
    if len(data_str) == 1:
        data_gen = Path(data_str[0]).iterdir()
        print(*[str(data).split('/')[-1] for data in data_gen])
