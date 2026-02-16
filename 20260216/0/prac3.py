from pathlib import Path
import zlib
import sys
for data in Path(sys.argv[1]).glob('.git/objects/??/*'):
    print(zlib.decompress(data.read_bytes()).partition(b'\x00'))
    print()