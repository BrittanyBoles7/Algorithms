def mtrf(C, m):
    n = len(C)
    F = [float('inf')] * (n + 1)
    F[1] = 0 

    for i in range(1, n):
        F[i + 1] = min(F[i + 1], F[i] + 1)

    for i, j, p in m:
        F[j] = min(F[j], F[i] + p)  

    for i in range(1,n):
        F[i + 1] = min(F[i + 1], F[i] + 1)

    return F[n]

if __name__ == "__main__": 
    cities = [1, 2, 3, 4, 5]  
    fares = [(1, 4, 2), (2, 5, 3)]  
    print(mtrf(cities, fares))