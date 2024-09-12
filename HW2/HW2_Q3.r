# calculate the nth smallest median between two arrays of the same size

smallest_median_value <- function(A, B, n) {
    if (n == 1) {
        return(min(A[1], B[1]))  #base case
    }
  
    k <- floor(n/2) #starting median
    
    if (A[k] < B[k]) {
        return(smallest_median_value(A[(k+1):n], B, n - k))
    } else {
        return(smallest_median_value(A, B[(k+1):n], n - k))
    }
}

A <- c(3, 5, 7, 9)
B <- c(2, 4, 6, 8)
n <- length(A)

smallest_median_value(A, B, n)

A <- c(6, 8, 13, 15, 19)
B <- c(3, 7, 10, 11, 16)
n <- length(A)

smallest_median_value(A, B, n)
