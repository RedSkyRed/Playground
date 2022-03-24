# Part 1
def trainer(wordlist, word, marker):
    """
    Identifies the possible word matches, from a given wordlist, which is useful for games such as Wordle.

    Parameters:
    - wordlist: array of str
        The possible words that the function will check
    - word: str
        The guessed word
    - marker: array of int
        A list of 0 and 1s, that tell us how close the guessed word is too the actual word.

    Output:
    Returns an array of all possible words from the wordlist that fit the marker and the word

    Worst-Case Time Complexity
    O(NM), where N is the number of strings/words and M is the length of each of those strings.
    
    Worst-Case Auxiliary-Space Complexity
    O(NM), where N is the number of strings/words and M is the length of each of those strings.
    """

    radix_string_sort(wordlist)

    potential_words = wordlist
    yellow_letters = []

    # We need to add all the letters that were in wrong spots into a list.
    for i in range(len(marker)):
        if marker[i] == 0:
            yellow_letters.append(word[i])

    # We then iterate through the list M amounts of time, where M is the length of the strings in the wordlist.
    for i in range(len(marker)):
        if marker[i]==1:
            potential_words = [x for x in potential_words if x[i] == word[i]]
        elif marker[i]==0:
            potential_words = [x for x in potential_words if x[i] in yellow_letters and x[i] != word[i]]

    return(potential_words)

def radix_string_sort(arry):
    """
    Radix sort built specifically to sort an array of strings. Does this by using ord, on letters before intiating count_sort.

    Parameters
    - arry: array of str
        The array of strings that we want to radix sort.
    
    Worst-Case Time Complexity
    O(26NM), where N is the number of strings/words and M is the length of each of those strings.
    
    Worst-Case Auxiliary-Space Complexity
    O(NM), where N is the number of strings/words and M is the length of each of those strings.
    """

    # i below represents the index, of the counting sort we are doing. We are moving from the rightmost index to the leftmost.
    for i in range(len(arry[0])-1,-1,-1):
        counting_string_sort(arry, i)

def counting_string_sort(arry, i):
    """
    Applies a counting sort algorithm, specifically to a list of strings, at a given index.
    Stable and to be used alongside radix_string_sort.

    Parameters:
    - arry: array of str
        An array of strings, with equal length
    - i: int
        The index to which counting sort will be applied too

    Worst-Case Time Complexity:
    O(26N), where N is the number of strings/words

    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of strings/words
    """
    
    n = len(arry)
    count = [0] * 26
    position = [0] * 26
    output = [0] * n
    
    # Filling up our count array
    for a in range(n):
        count[ord(arry[a][i])-97] += 1
        
    # Filling in our position array
    for a in range(1,26):
        position[a] = position[a-1] + count[a-1]

    # Now to fill in our output.
    for a in range(n):
        output[position[ord(arry[a][i])-97]] = arry[a]
        position[ord(arry[a][i])-97] += 1

    # Not to make our array equal to our output
    for a in range(n):
        arry[a] = output[a]


# Part 2
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