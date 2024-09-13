# calculate the nth smallest median between two arrays of the same size

smallest_median_value <- function(A, B) {
  n <- length(A)  
  if (n == 1) {
        return(min(A[n], B[n]))  #base case
    }
  
    k <- floor(n/2) #starting median
    
    if (A[k] < B[k]) {
        return(smallest_median_value(A[(k+1):n], B[1:(n-k)]))
    } else {
        return(smallest_median_value(A[1:(n-k)], B[(k+1):n]))
    }
}

A <- c(3, 5, 7, 9)
B <- c(2, 4, 6, 8)

smallest_median_value(A, B) 

A <- c(6, 8, 13, 15, 19)
B <- c(3, 7, 10, 11, 16)

smallest_median_value(A, B)

A <- c(1,4,8,12,20,25,50,65,67,79)
B <- c(2,3,5,19,21,28,40,59,70,80)

smallest_median_value(A, B)




