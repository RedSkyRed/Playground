def local_maximimum(matrix):
    """
    Finds a local maximum within a matrix.

    Parameters:
    - matrix: arrays within an array
    A matrix represented by a series of arrays

    Output:
    Returns the coordinates of the local maximum in the matrix.

    Worst-Case Time Complexity
    O(n), where n is the length or height of the matrix.
    
    Worst-Case Auxiliary-Space Complexity
    O(1)
    """

    length_of_matrix = len(matrix)-1
    height_of_matrix = len(matrix[0])

    # Similiar to binary sort, the left and right most markers, indicate where our local maximum must lie between
    left_m = 0
    right_m = length_of_matrix

    local_maximum_found = None

    # Each iteration, this loop finds the midpoint, and cuts down all the possible locations of a local maximum by half.
    while local_maximum_found == None:
        mid = left_m + (right_m - left_m)// 2
        vertical_max_index = 0
        vertical_max = matrix[vertical_max_index][mid]
        for i in range(1,height_of_matrix):
            if vertical_max < matrix[i][mid]:
                vertical_max = matrix[i][mid]
                vertical_max_index = i
        # These conditionals, check whether or not the number is on the edge of our matrix and if they are local maximums
        if mid == 0 and vertical_max > matrix[vertical_max_index][mid+1]:
            local_maximum_found = [vertical_max_index,mid]
        elif mid == length_of_matrix and vertical_max > matrix[vertical_max_index][mid-1]:
            local_maximum_found = [vertical_max_index,mid]
        # This just checks if the highest value found thus far, is a local maximum
        elif vertical_max > matrix[vertical_max_index][mid-1] and vertical_max > matrix[vertical_max_index][mid+1]:
            local_maximum_found = [vertical_max_index,mid]
        # These conditionals help move our markers, and help narrow down where our local maximum may be.
        elif matrix[vertical_max_index][mid-1] > matrix[vertical_max_index][mid]:
            right_m = mid-1
        elif matrix[vertical_max_index][mid+1] > matrix[vertical_max_index][mid]:
            left_m = mid+1
        
    return local_maximum_found