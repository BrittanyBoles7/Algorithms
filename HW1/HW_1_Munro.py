import random as rand
from matplotlib import pyplot as plt
import time
import os
from scipy.interpolate import make_interp_spline
import numpy as np
# Group: Madie Munro, Redempta Manzi, Brittany Boles
#-------------------------------------------------------------------------------------------------------------------------------------------
#Naive approach to polynomial multiplication
def poly_mult_naive(P, Q):

    #initialize the product polynomial
    product = [0] * (len(P) + len(Q) - 1)

    #multiply the two polynomials, then update the product value
    for i in range(len(P)):
        for j in range(len(Q)):
            product[i+j] += P[i] * Q[j]
    return product

#-------------------------------------------------------------------------------------------------------------------------------------------
#Simple Divide-and-Conquer approach to polynomial multiplication
def poly_mult_simple_dac(P, Q):

    #pad out poly list with zeros in case one poly is shorter than the other
    P_len = len(P)
    Q_len = len(Q)
    if P_len < Q_len:
        P += [0] * (Q_len - P_len)
    elif P_len > Q_len:
        Q += [0] * (P_len - Q_len)

    #base case
    n = len(P)
    if (n == 1):
        return [P[0] * Q[0]]
    
    #implement the n/2 property of this algorithm (i.e., split both polynomials in half)
    m = n // 2
    P_lower = P[:m]
    P_higher = P[m:]
    Q_lower = Q[:m]
    Q_higher = Q[m:]

    #use recursion to multiply the split polynomials (similar to Strassen's algorithm for matrix multiplication)
    temp_poly_1 = poly_mult_simple_dac(P_lower, Q_lower) #equivilent to A_0(x)B_0(x) in the DaC alg
    temp_poly_2 = poly_mult_simple_dac([i + j for i, j in zip(P_lower, P_higher)], [i + j for i, j in zip(Q_lower, Q_higher)]) #equivilent to x^(n/2)*(A_1(x)B_0(x) + A_0(x)B_1(x)) in the DaC alg
    temp_poly_3 = poly_mult_simple_dac(P_higher, Q_higher) #equivilent to x^n*A_1(x)B_1(x) in the DaC alg

    #initialize the product polynomial
    product = [0] * (2 * n - 1)

    #combine the recursed solutions into one product

    for i in range(len(temp_poly_1)):
        product[i] += temp_poly_1[i]

    for i in range(len(temp_poly_2)):
        product[i+m] += temp_poly_2[i] - temp_poly_1[i] - temp_poly_3[i]

    for i in range(len(temp_poly_3)):
        product[i + 2 * m] += temp_poly_3[i]

    #remove padding (otherwise it adds an extra polynomial 0x^n+1)
    while len(product) > 1 and product[-1] == 0:
        product.pop()

    #return product
    return product

#-------------------------------------------------------------------------------------------------------------------------------------------
#format the polynomials into a printable format ([1,2,3] to 1 + 2x + 3x^2)
def poly_str_print(P):
    poly_str = ""
    for i in range(len(P)):
        poly_str += str(P[i])
        if (i != 0):
            poly_str += "x^"
            poly_str += str(i)
        if (i != len(P) - 1):
            poly_str += " + "
    print(poly_str)

#-------------------------------------------------------------------------------------------------------------------------------------------
#print out runtimes for the two algorithm approaches
def print_alg_times():

    sizes = [1, 5, 10, 25, 50, 75, 100, 200, 500, 800, 1000, 2000, 3500, 5000, 7000, 8500, 10000]  #different polynomial degrees
    naive_times = [] #store times for naive approach here
    dac_times = [] #store time for DaC approach here

    for size in sizes:
        #create random polynomials of the given degree
        poly_1 = [rand.randint(1, 50) for _ in range(size)] 
        poly_2 = [rand.randint(1, 50) for _ in range(size)]

        #measure time for algorithm execution - Naive
        start_naive = time.time()
        poly_mult_naive(poly_1, poly_2)
        end_naive = time.time()
        naive_avg = end_naive - start_naive

        #measure time for algorithm execution - Divide-and-Conquer
        start_dac = time.time()
        poly_mult_simple_dac(poly_1, poly_2)
        end_dac = time.time()
        dac_avg = end_dac - start_dac

        #store times calculated
        naive_times.append(naive_avg)
        dac_times.append(dac_avg)

    #smooth lines with interpolation
    interp_sizes = np.linspace(min(sizes), max(sizes), 500)

    naive_smooth = make_interp_spline(sizes, naive_times)(interp_sizes)
    dac_smooth = make_interp_spline(sizes, dac_times)(interp_sizes)
    
    #plot and save the results
    plt.figure(figsize=(12, 8))
    plt.plot(interp_sizes, naive_smooth, label="Naive Approach", marker="o")
    plt.plot(interp_sizes, dac_smooth, label="Divide-and-Conquer", marker="o")
    plt.xlabel("Polynomial Degree")
    plt.ylabel("Algorithm Runtime (seconds)")
    plt.title("Polynomial Multiplication Algorithms: Naive vs. Divide-and-Conquer")
    plt.legend()
    plt.grid(True)

    path = os.path.dirname(__file__)
    file = "runtimes_munro.png"
    plt.savefig(os.path.join(path, file))
    plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------------

def main():

    #test the two algorithms
    poly_1 = [1,3,1]#[8,3,1,15,0,9] #polynomials are sorted from lowest to highest order (ex: 8 + 3x + x^2 + 6x^3)
    poly_2 = [5,1,2]#[6,3,2,8,1,13] #(ex: 1 + 2x + 4x^2)

    #print out the polynomials
    print("Polynomial #1: ")
    poly_str_print(poly_1)
    print("\nPolynomial #2: ")
    poly_str_print(poly_2)

    #measure time for algorithm execution - Naive
    start_naive = time.time()
    poly_3 = poly_mult_naive(poly_1, poly_2)
    time.sleep(1) #added for better time readability
    end_naive = time.time()

    #measure time for algorithm execution - Divide-and-Conquer
    start_dac = time.time()
    poly_4 = poly_mult_simple_dac(poly_1, poly_2)
    time.sleep(1) #added for better time readability
    end_dac = time.time()

    #print the new polynomial multiplied (Naive)
    print("\n\nNew polynomial after multiplication (Naive approach): ")
    poly_str_print(poly_3)
    #print the new polynomial multiplied (DaC)
    print("\nNew polynomial after multiplication (Simple Divide-and-Conquer approach): ")
    poly_str_print(poly_4)

    #print the time for the naive approach
    print(f"\n\nRuntime of Naive Approach: {end_naive - start_naive}")
    #print the time for the DaC approach
    print(f"\nRuntime of Divide-and-Conquer Approach: {end_dac - start_dac}")

    #print simulated algorithm runtimes as a plot
    print_alg_times()

#-------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()