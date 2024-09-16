#modified count sort

def bucket_sort(input_array):

    max_elmt = max(input_array) #calculate the min value in the array
    min_elmt = min(input_array) #calculate the max value in the array
    D = max_elmt - min_elmt #calculate D

    #adjust each element in the array to mirror the calculation of D
    for i in range(0, len(input_array)):
        input_array[i] = input_array[i] - min_elmt

    #initialize a count array with 0
    count_array = [0] * (D + 1)

    #map each element of input_array as an index of count_array
    for num in input_array:
        count_array[num] += 1

    #calculate prefix sum at every index of count_array
    for i in range(1, D + 1):
        count_array[i] += count_array[i - 1]

    #create output_array that will serve as the sorted input array
    output_array = [0] * len(input_array)

    #build the output array in reverse order to maintain stability
    for i in range(len(input_array) - 1, -1, -1):
        output_array[count_array[input_array[i]] - 1] = input_array[i] + min_elmt #add back the min value
        count_array[input_array[i]] -= 1

    return output_array

if __name__ == "__main__":
    input_array = [5,9,4,10,8,7,15,13]
    output_array = bucket_sort(input_array)
    for num in output_array:
        print(num, end=" ")
