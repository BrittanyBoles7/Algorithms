import numpy as np

def edit_distance(s, t, delta, alpha):
    n = len(s)
    m = len(t)
    dist_arr = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dist_arr[i][0] = i * delta
    for j in range(m + 1):
        dist_arr[0][j] = j * delta
    for j in range(1,m+1):
        for i in range(1,n+1):
            if s[i-1] == t[j - 1]:
                dist_arr[i][j] = dist_arr[i-1][j-1]
            else:
                dist_arr[i][j] = min(dist_arr[i][j - 1] + delta, dist_arr[i - 1][j] + delta, dist_arr[i - 1][j - 1] + alpha)
    for row in dist_arr:
        print(" ".join(map(str, row)))
    return dist_arr[n][m]

if __name__ == "__main__":
    str1 = "SPIRE"
    str2 = "TIRED"
    print("Edit Distance:", edit_distance(str1, str2, 1, 1))
