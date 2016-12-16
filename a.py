import sys
 
def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words

def count_words(filename):
    res = {}
    mas = read_words(filename)
    for i in mas:
        i = i.lower()
        if i not in res:
            res[i] = 1
        else:
            res[i] += 1
    return res

def print_words(filename):
    res = count_words(filename)
    for key in sorted(res):
        print('{}:{}'.format(key, res[key]))
        
def print_top(filename):
    res = count_words(filename)
    d = list(res.items())
    d.sort(key = lambda x: x[1], reverse = True)
    lenght = min(len(d), 20)
    for i in range(lenght):
        print('{}:{}'.format(d[i][0], d[i][1]))

def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)
if __name__ == "__main__":
    main()
