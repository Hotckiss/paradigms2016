def verbing(s):
    l = len(s)
    if l < 3:
        return s
    else:
        if(s[l - 3: l] == 'ing'):
            s = s[0: l - 3] + 'ly'
        else:
            s = s + 'ing'
    return s

def not_bad(s):
    l = len(s)
    n = s.find('not')
    b = s.find('bad')
    
    if n != -1 and b != -1 and n < b:
        s = s[0:n] + 'good' + s[b + 3: l]
    return s

def front_back(a, b):
    la = len(a)
    lb = len(b)
    ma = (la + 1) // 2
    mb = (lb + 1) // 2
    return a[0: ma] + b[0: mb] + a[ma: la] + b[mb: lb]
