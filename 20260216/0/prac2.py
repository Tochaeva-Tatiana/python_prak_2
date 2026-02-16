from pathlib import Path
import zlib
import sys

data = sorted(Path(sys.argv[1]).glob('.git/objects/??/*'))
print(data)