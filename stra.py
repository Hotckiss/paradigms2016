import numpy as np
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
    T1 = strassen(A11 + A22, B11 + B22)
    T2 = strassen(A21 + A22, B11)
    T3 = strassen(A11, B12 - B22)
    T4 = strassen(A22, B21 - B11)
    T5 = strassen(A11 + A12, B22)
    T6 = strassen(A21 - A11, B11 + B12)
    T7 = strassen(A12 - A22, B21 + B22)
    C11 = T1 + T4 - T5 + T7
    C21 = T2 + T4
    C12 = T3 + T5
    C22 = T1 + T3 - T2 + T6
    return np.vstack((np.hstack((C11,C12)), np.hstack((C21,C22))))

def main():
    n = int(input())
    A = []
    B = []

    for i in range(n):
        A.append(list(map(int, input().split())))
    A = np.matrix(A)
    for i in range(n):
        B.append(list(map(int, input().split())))
    B = np.matrix(B)
    if (n & (n - 1)) != 0:
        new_size = 2 ** (int(math.log2(n)) + 1)
        A = np.hstack((A, np.zeros((n,new_size - n))))
        A = np.vstack((A, np.zeros((new_size - n,new_size))))
        B = np.hstack((B, np.zeros((n,new_size - n))))
        B = np.vstack((B, np.zeros((new_size - n,new_size))))
    C = strassen(A, B)
    C = C[:n, :n]
    C = C.tolist()
    for i in range(len(C)):
        for j in range(len(C[i])):
            print(int(C[i][j]), end = ' ')
        print('\n', end = '')

if __name__ == "__main__":
    main()
   
