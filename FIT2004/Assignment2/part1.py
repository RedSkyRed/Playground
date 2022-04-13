def ideal_place(relevant):
    desired_place = [mid_most_location(relevant, 0),mid_most_location(relevant, 1)]
    return desired_place

# will need to change this functions name
def mid_most_location(datapoints, axis_index):
    length_of_arry = len(datapoints)
    median_index = length_of_arry//2
    arry_on_axis = []
    for i in range(0, length_of_arry):
        arry_on_axis.append(datapoints[i][axis_index])
    desired_value = quick_select(arry_on_axis, 0, length_of_arry-1, median_index)
    return desired_value


#with median of medians\
# Heavily inspired by the lectures
def quick_select(arry, lo, hi, k):
    if len(arry)== 1:
        return arry[k]
    pivot = median_of_medians(arry)
    mid = partition(arry, lo, hi, pivot)
    if mid > k:
        return quick_select(arry, lo, mid-1, k)
    elif k > mid:
        return quick_select(arry, mid+1, hi, k)
    else:
        return arry[k]


# Heavily inspired by the lectures
def median_of_medians(arry):
    n = len(arry)
    if n <= 5:
        return insertion_sort_median(arry)
    medians = []
    for i in range(0,n//5):
        medians.append(insertion_sort_median(arry[5*i:5*i+5]))
    return quick_select(medians, 0, len(medians), len(medians)//2)    

def insertion_sort_median(arry):
    arry_length = len(arry)
    for i in range (1, arry_length):
        pointer = arry[i]
        j = i-1
        while j >= 0 and pointer < arry[j]:
            arry[j + 1] = arry[j]
            j -= 1
        arry[j + 1] = pointer
    return arry[arry_length//2]


# Heavily inspired by the lectures
# This was a pain in the ass and very similiar to another partitioning algorithm I found online.
def partition(arry, lo, hi, pivot):
    for i in range(lo, hi):
        if arry[i] == pivot:
            swap(arry, hi, i)
            break
 
    x = arry[hi]
    i = lo
    for j in range(lo, hi):
        if (arry[j] <= x):
            swap(arry, i, j)
            i += 1
    swap(arry, i, hi)
    return i

def swap(arry, i, j):
    arry[i],arry[j] = arry[j],arry[i]

relevant = [[5,8],[7,9],[9,1],[0,1],[1,9],[2,1]]

print(ideal_place(relevant)) 