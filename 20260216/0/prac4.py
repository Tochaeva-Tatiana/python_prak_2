from pathlib import Path
import zlib
import sys
for data in Path(sys.argv[1]).glob('.git/objects/??/*'):
    data2 = zlib.decompress(data.read_bytes()).partition(b'\x00')
    if 'tree' in str(data2[0]):
        print(data2)