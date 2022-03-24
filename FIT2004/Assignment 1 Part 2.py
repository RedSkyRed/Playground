from contextlib import nullcontext


def local_maximimum(matrix):
    length_of_matrix = len(matrix)-1
    height_of_matrix = len(matrix[0])-1

    left_m = 0
    right_m = length_of_matrix
    local_maximum_found = None

    while local_maximum_found == None:
        mid = left_m + (right_m - left_m)// 2
        vertical_max_index = 0
        vertical_max = matrix[vertical_max_index][mid]
        for i in range(1,height_of_matrix):
            if vertical_max < matrix[i][mid]:
                vertical_max = matrix[i][mid]
                vertical_max_index = i
        if mid == 0 and vertical_max > matrix[vertical_max_index][mid+1]:
            local_maximum_found = [vertical_max_index,mid]
        elif mid == length_of_matrix and vertical_max > matrix[vertical_max_index][mid-1]:
            local_maximum_found = [vertical_max_index,mid]
        elif vertical_max > matrix[vertical_max_index][mid-1] and vertical_max > matrix[vertical_max_index][mid+1]:
            local_maximum_found = [vertical_max_index,mid]
        elif matrix[vertical_max_index][mid-1] > matrix[vertical_max_index][mid]:
            right_m = mid-1
        elif matrix[vertical_max_index][mid+1] > matrix[vertical_max_index][mid]:
            left_m = mid+1
        
    return local_maximum_found

M = [[1,2,27,28,29,30,49],
    [3,4,25,26,31,32,48],
    [5,6,23,24,33,34,47],
    [7,8,21,22,35,36,46],
    [9,10,19,20,37,38,45],
    [11,12,17,18,39,40,44],
    [13,14,15,16,41,42,43]]

M1 = [[1,3,6,10,15,21,28],
    [2,5,9,14,20,27,34],
    [4,8,13,19,26,33,39],  
    [7,12,18,25,32,38,90],
    [11,17,24,31,37,57,91],
    [99,98,97,60,59,58,56,],
    [22,29,35,40,44,55,49]]

print(local_maximimum(M1))