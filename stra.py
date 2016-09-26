import numpy
import math
def strassen(A, B):
    n = len(A)
    if n == 1:
        return A * B
    n = n // 2
    A11 = A[:n, :n]
    A12 = A[:n, n:]
    A21 = A[n:, :n]
    A22 = A[n:, n:]
    B11 = B[:n, :n]
    B12 = B[:n, n:]
    B21 = B[n:, :n]
    B22 = B[n:, n:]
    P1 = strassen(A11 + A22, B11 + B22)
    P2 = strassen(A21 + A22, B11)
    P3 = strassen(A11, B12 - B22)
    P4 = strassen(A22, B21 - B11)
    P5 = strassen(A11 + A12, B22)
    P6 = strassen(A21 - A11, B11 + B12)
    P7 = strassen(A12 - A22, B21 + B22)
    C11 = P1 + P4 - P5 + P7
    C21 = P2 + P4
    C12 = P3 + P5
    C22 = P1 + P3 - P2 + P6
    return numpy.vstack((numpy.hstack((C11,C12)), numpy.hstack((C21,C22))))

def main():
    n = int(input())
    ns = 2 ** math.ceil(math.log2(n))
    A = numpy.zeros((ns, ns), dtype = numpy.int)
    B = numpy.zeros((ns, ns), dtype = numpy.int)
    a = []
    b = []
    
    for i in range(n):
        a.append(list(map(int, input().split())))
    for i in range(n):
         b.append(list(map(int, input().split())))
         
    a = numpy.matrix(a)
    b = numpy.matrix(b)
    A[:n, :n] = a
    B[:n, :n] = b
    
    C = strassen(A, B)
    C = C[:n, :n]
    for row in C:
        print(' '.join(list(map(str, row))))
if __name__ == "__main__":
    main()
   
