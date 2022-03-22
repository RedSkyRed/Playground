
def trainer(wordlist, word, marker):
    
    radix_string_sort(wordlist)
    potential_words = wordlist
    # parition list
    yellow_letters = []

    for i in range(len(marker)):
        if marker[i] == 0:
            yellow_letters.append(word[i])

    for i in range(len(marker)):
        if marker[i]==1:
            potential_words = [x for x in potential_words if x[i] == word[i]]
        elif marker[i]==0:
            potential_words = [x for x in potential_words if x[i] in yellow_letters and x[i] != word[i]]

    return(potential_words)

                

# List Sorting Algorithm
#--------------------------------------
def radix_string_sort(arry):
    for i in range(len(arry[0])-1,-1,-1):
        counting_string_sort(arry, i)

def counting_string_sort(arry, i):
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
#-------------------------------------------------
wordlist1 = ['limes', 'spare', 'store', 'loser', 'aster', 'pares', 'taser', 'pears', 'stare', 'spear', 'parse', 'reaps', 'rates', 'tears', 'losts']

print(trainer(wordlist1, 'spare', [1,1,0,0,1]))


#-------------------------------------------------
#Testcases
# testcase1 = ['aars', 'azrs', 'abas', 'abbe', 'abca', 'abbs']

# print(testcase1[0][3])
# print(len(testcase1))

# radix_string_sort(testcase1)

