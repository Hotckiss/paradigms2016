import sys
import os
from hashlib import sha1
def hashfile(name):
    with open(name, 'rb') as f:
            m = sha1()
            while True:
                data = f.read(1024)
                if not data:
                    break
                m.update(data)
    return m.hexdigest()

def walker(dir, dct):
  for name in os.listdir(dir):
    path = os.path.join(dir, name)
    if os.path.islink(path):
        pass
    if os.path.isfile(path):
        if name[0] == '.' or name[0] == '~':
            pass
        else:
            k = hashfile(path)
            if dct.get(k) == None:
                dct[k] = []
            dct[k].append("{}".format(path))
    else:
        walker(path, dct)
        
if __name__ == "__main__":
    dct = {}
    walker("tst", dct)
    for key in dct:
        for i in range(len(dct[key]) - 1):
            print(dct[key][i], end = ':')
        print(dct[key][len(dct[key]) - 1])
