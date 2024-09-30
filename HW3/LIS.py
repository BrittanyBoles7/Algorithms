import numpy as np

def lis(A):
    n = len(A)
    lis_arr = [1] * (n+1)
    for i in range(1,n):
        for j in range(i):
            if A[i] > A[j]:
                lis_arr[i] = max(lis_arr[j]+1, lis_arr[i])
    return max(lis_arr)

if __name__ == "__main__":
    # arr = np.random.randint(50, size=25)
    arr = [3,6,8,10,1,3,15,2,4]
    print(arr)
    print(lis(arr))
