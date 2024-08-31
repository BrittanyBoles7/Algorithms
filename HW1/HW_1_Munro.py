import random as rand
from matplotlib import pyplot as plt
import time
import os

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
    P_len, Q_len = len(P), len(Q)
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
    P_low = P[:m]
    P_high = P[m:]
    Q_low = Q[:m]
    Q_high = Q[m:]

    #use recursion to multiply the split polynomials (similar to Strassen's algorithm for matrix multiplication)
    temp_poly_1 = poly_mult_simple_dac(P_low, Q_low) #equivilent to A_0(x)B_0(x) in the DaC alg
    temp_poly_2 = poly_mult_simple_dac([x + y for x, y in zip(P_low, P_high)], [x + y for x, y in zip(Q_low, Q_high)]) #equivilent to x^(n/2)*(A_1(x)B_0(x) + A_0(x)B_1(x)) in the DaC alg
    temp_poly_3 = poly_mult_simple_dac(P_high, Q_high) #equivilent to x^n*A_1(x)B_1(x) in the DaC alg

    #initialize the product polynomial
    product = [0] * (2 * n -1)

    #combine the recursed solutions into one product
    for i in range(len(temp_poly_1)):
        product[i] += temp_poly_1[i]

    for i in range(len(temp_poly_2)):
        product[i + m] += temp_poly_2[i]
        if i < len(temp_poly_1):
            product[i + m] -= temp_poly_1[i]
        if i < len(temp_poly_3):
            product[i + m] -= temp_poly_3[i]

    for i in range(len(temp_poly_3)):
        product[i + 2 * m] += temp_poly_3[i]

    #remove padding (otherwise it add an extra polynomial of 0x^n+1)
    while len(product) > 1 and product[-1] == 0:
        product.pop()

    #return product
    return product

#-------------------------------------------------------------------------------------------------------------------------------------------
#format the polynomials into a printable format ([1,2,3] to 1 + 2x + 3x^2)
def poly_str_print(P):
    for i in range(len(P)):
        print(P[i], end = "")
        if (i != 0):
            print("x^", i, end = "")
        if (i != len(P) - 1):
            print(" + ", end = "")

#-------------------------------------------------------------------------------------------------------------------------------------------
#print out runtimes for the two algorithm approaches
def print_alg_times():

    sizes = [2, 4, 8, 16, 32, 64, 128, 256]  #different polynomial sizes
    naive_times = [] #store times for naive approach here
    dac_times = [] #store time for DaC approach here

    for size in sizes:
        #create random polynomials of the given size
        poly_1 = [rand.randint(1, 10) for _ in range(size)] 
        poly_2 = [rand.randint(1, 10) for _ in range(size)]

        #measure time for algorithm execution - Naive
        start_naive = time.time()
        poly_mult_naive(poly_1, poly_2)
        end_naive = time.time()

        #measure time for algorithm execution - Divide-and-Conquer
        start_dac = time.time()
        poly_mult_simple_dac(poly_1, poly_2)
        end_dac = time.time()

        #store times calculated
        naive_times.append(end_naive - start_naive)
        dac_times.append(end_dac - start_dac)

    #plot and save the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, naive_times, label="Naive Approach", marker="o")
    plt.plot(sizes, dac_times, label="Divide-and-Conquer", marker="o")
    plt.xlabel("Polynomial Size")
    plt.ylabel("Runtime (seconds)")
    plt.title("Polynomial Multiplication: Naive vs. Divide-and-Conquer")
    plt.legend()
    plt.grid(True)

    path = os.path.dirname(__file__)
    file = "runtimes_munro.png"
    plt.savefig(os.path.join(path, file))
    plt.show()

#-------------------------------------------------------------------------------------------------------------------------------------------

def main():

    #test the two algorithms
    poly_1 = [5,0,10,6] #polynomials are sorted from lowest to highest order (ex: 5 + x + 10x^2 + 6x^3)
    poly_2 = [1,2,4]

    #print out the polynomials
    print("Polynomial #1: ")
    poly_str_print(poly_1)
    print("\nPolynomial #2: ")
    poly_str_print(poly_2)

    #measure time for algorithm execution - Naive
    start_naive = time.time()
    poly_3 = poly_mult_naive(poly_1, poly_2)
    time.sleep(1)
    end_naive = time.time()

    #measure time for algorithm execution - Divide-and-Conquer
    start_dac = time.time()
    poly_4 = poly_mult_simple_dac(poly_1, poly_2)
    time.sleep(1)
    end_dac = time.time()

    #print the new polynomial multiplied (Naive)
    print("\n\nNew polynomial after multiplication (Naive approach): ")
    poly_str_print(poly_3)
    #print the new polynomial multiplied (DaC)
    print("\nNew polynomial after multiplication (Simple Divide-and-Conquer (Strassen) approach): ")
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