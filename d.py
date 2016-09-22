import sys
import os
from hashlib import sha1
from collections import defaultdict
def hashfile(name):
    with open(name, 'rb') as f:
            h = sha1()
            while True:
                data = f.read(1024)
                if not data:
                    break
                h.update(data)
    return h.hexdigest()
def main():
    if len(sys.argv) != 2:
        print('usage: ./d.py file')
        sys.exit(1)
    dct = defaultdict(list)
    for d, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            if f[0] == '.' or f[0] == '~':
                pass
            else:
                path = os.path.join(d, f)
                dct[hashfile(path)].append("{}".format(path))
    for value in dct.values():
        print(*value, sep = ':')    
if __name__ == "__main__":
    main()
