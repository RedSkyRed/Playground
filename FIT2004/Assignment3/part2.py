def hero(attacks):
    # Create Graph as a linked list
    # zero represents are starting value! everything can reach the node 0
    graph_attacks = [[]]
    for i in range(len(attacks)):
        graph_attacks[0].append([attacks[i][0],attacks[i][3]])
        graph_attacks.append([])

# Fills in the direct graph
    for u in range(len(attacks)-1):
        for v in range(u+1,len(attacks)):
            # If they don't overlap
            if (attacks[u][1] <= attacks[v][2] and attacks[v][1] <= attacks[u][2]) == False:
                if attacks[u][1] < attacks[v][1]:
                    graph_attacks[u+1].append([attacks[v][0],attacks[v][3]])
                else: 
                    graph_attacks[v+1].append([attacks[u][0],attacks[u][3]])
    
    return critical_path(graph_attacks)

def critical_path(adj_list):
    dp = [0]*len(adj_list)
    pred = [0]*len(adj_list)
    visited = [False]*len(adj_list)

    for i in range(len(adj_list)):
        if visited != True:
            dfs(adj_list, dp, visited, pred, i)

    
    #Longest path
    optimal_attacks = []
    backtracking = pred[0]
    while backtracking != 0:
        optimal_attacks.append(attacks[backtracking-1])
        backtracking = pred[backtracking]
    return optimal_attacks

# Note j[0] represents the node that is a neighbour, where as j[1] represents the weight of the node
def dfs(adj_list, dp, visited, pred, i):
    if visited[i] == True:
        return
    else:
        visited[i] == True
    # Check the neighbours
    for j in adj_list[i]:
        if visited[j[0]] == False:
            dfs(adj_list, dp, visited, pred, j[0])
    # Once recursion hits bottom
        if dp[j[0]]+j[1] > dp[i]:
            pred[i] = j[0]
        dp[i] = max(dp[i], dp[j[0]]+j[1])


def find_max_index(arry):
    max_value = 0
    index = 0
    for i in range(0,len(arry)):
        if arry[i] > max_value:
            max_value = arry[i]
            index = i
    return index


attacks = [[1,1,100,7], [2,4,100,8], [3,23,100,12], [4,31,100,6], [5,51,100,9]]
expected_res = [[3,23,100,12]]

print(hero(attacks))