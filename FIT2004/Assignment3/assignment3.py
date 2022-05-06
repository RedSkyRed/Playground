# Part 1
def best_revenue(revenue, travel_days, start):
    """
    Returns the maximum possible revenue that can be generated, given a starting place

    Parameters:
    - revenue: list of lists
        revenue[z][x], where z is representative of the day and x is representative of the city and the number returned is the revenue 
        generated at a particular city, on a certain day
    - travel_days: a list of lists
        travel_days[x][y], where x is representative of a city, y is representative of the city we want to travel too, and the number
        returned is the number of days it would take to get there, if there is a road there.
    - start: an int
        the city we start from

    Output:
    Returns a single int, which represents the max revenue gained by starting from one city

    Worst-Case Time Complexity
    O(N^2(D+N)), where N is the number of cities, and D is the number of days.
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of cities
    """
    max_days = len(revenue)
    max_cities = len(revenue[-1])
    # Each index in profit, represents the index of a city.
    profit = [float('-inf')] * max_cities
    profit[start] = 0
    # Retains a copy of the max profit a city could have made on previous days.
    previous_days_profit = []

    # Days loop
    for d in range(0,max_days):
        # Daily update
        # Update each city that has been visited with the revenue that they would make staying at the city.
        previous_days_profit.append(profit.copy())   
        for x in range(max_cities):
            if profit[x] != float('inf'):
                profit[x] += revenue[d][x]
        # Bellman loop
        bellman_ford(travel_days, profit, d, max_cities, previous_days_profit)
        

    # Max value after doing bellmans
    max_revenue = find_max(profit)
    return max_revenue


def bellman_ford(travel_days, profit, day, max_cities, previous_d_profit):
    """
    Finds the maximum profit each city could make on a given day, factoring in previous days.

    Parameters:
    - revenue: list of lists
        revenue[z][x], where z is representative of the day and x is representative of the city and the number returned is the revenue 
        generated at a particular city, on a certain day
    - travel_days: a list of lists
        travel_days[x][y], where x is representative of a city, y is representative of the city we want to travel too, and the number
        returned is the number of days it would take to get there, if there is a road there.
    - day: an int
        The current day that we want to check
    - max_cities: an int
        The number of cities present
    - previous_d_profits: a list of lists
        Contains the maximum amount of profits made by cities on previous days

    Worst-Case Time Complexity
    O(N^2(N)), where N is the number of cities
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of cities
    """
    # Used for efficiency to check if anything has changed from the previous loop
    changes = True
    for i in range(max_cities-1):
        # If there are no changes made last loop, break early
        if changes == False:
            break
        else:
            changes = False

        # Go through all cities.
        for x in range(len(profit)):
            # If a city has not been initialized yet, don't do anything.
            if profit[x] != float('-inf') and profit[x] != 0:
                # Check all possible places that we can travel too from our city.
                for y in range(len(travel_days[x])):
                    route_length = travel_days[x][y]
                    # If enough days have passed, and the path exists
                    if route_length <= day + 1 and route_length != -1:
                        # Intialize the city if it hasn't been yet
                        if profit[y] == float('-inf'):
                            profit[y] = 0
                        # Else check if the sales person would make more money having travelled there later, or if he stayed.
                        elif previous_d_profit[day+1-route_length][x] > profit[y]:
                            profit[y] = previous_d_profit[day+1-route_length][x]
                    

def find_max(arry):
    """
    Returns the maximum possible value from an array

    Parameters:
    - arry: an array
        the array we want to look through to find the max value

    Output:
    Returns the maximum value from an array

    Worst-Case Time Complexity
    O(N), where N is the number of items in the array.
    
    Worst-Case Auxiliary-Space Complexity
    O(1), does not take up much space
    """
    max_value = arry[0]
    for i in range(1,len(arry)):
        if arry[i] > max_value:
            max_value = arry[i]
    return max_value

# --------------------------------------
# Part 2

def hero(attacks):
    """
    Returns the optimal list of attacks that our hero should defend.

    Parameters:
    - attacks: an array
        attacks[m, s, e, c], where m represents the multiverse, s represents the starting day, e represents the ending day and
        c represents the clones sent to attack said multiverse

    Output:
    Returns a list of attacks.

    Worst-Case Time Complexity
    O(NlogN), where N is the number of attacks
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of attacks

    Note:
    I wanted to create a weighted graph, so I could therefore use the longest path algorithm to determine the best
    attacks to defend against it.
    
    I first created my graph, and in order to ensure space complexity, I used an adjacency matrix, alongside making sure that the
    relationships between my nodes were sparse.
     
    Additionally my nodes, in my graph were the attacks, and any attack that didn't overlap with another attack, I placed a directed
    edge between the two nodes. Any path in my graph therefore represents a series of possible combination of attacks, and I then
    used the longest path to find out what the best path was.
    """
    # Here is my adjacency matrix
    graph_attacks = [[]]
    # I put a node that doesn't represent any attack as my first node.
    # This node can be reached by all attacks however. 
    for i in range(len(attacks)):
        graph_attacks[0].append([attacks[i][0],attacks[i][3]])
        graph_attacks.append([])

    # Fills in the direct graph with all the edges, and thier corresponding weights.
    for u in range(len(attacks)-1):
        for v in range(u+1,len(attacks)):
            # If they don't overlap
            if (attacks[u][1] <= attacks[v][2] and attacks[v][1] <= attacks[u][2]) == False:
                if attacks[u][1] < attacks[v][1]:
                    graph_attacks[u+1].append([attacks[v][0],attacks[v][3]])
                else: 
                    graph_attacks[v+1].append([attacks[u][0],attacks[u][3]])
    
    return critical_path(graph_attacks, attacks)

def critical_path(adj_list, attacks):
    """
    Not only finds the longest path in a graph, but also returns the nodes involved in said path.

    Parameters:
    - adj_list: a list of lists
        adj[x][y], where x represents a node, y represents another node and its corresponding weight to getting there.

    Output:
    Returns a list of nodes, that are a part of the longest path

    Worst-Case Time Complexity
    O(N), where N is the number of nodes
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of nodes
    """
    dp = [0]*len(adj_list)
    pred = [0]*len(adj_list)
    visited = [False]*len(adj_list)

    # Recursive call that ignores nodes that have been visited
    for i in range(len(adj_list)):
        if visited != True:
            dfs(adj_list, dp, visited, pred, i)

    #Longest path
    nodes_in_longest_path = []
    backtracking = pred[0]
    # Runs through the predecessor lists, and adds the nodes to our list, until we have reached the source node.
    while backtracking != 0:
        nodes_in_longest_path.append(attacks[backtracking-1])
        backtracking = pred[backtracking]
    return nodes_in_longest_path


def dfs(adj_list, dp, visited, pred, i):
    """
    Recursively searchs through all nodes, and updates our dp.

    Parameters:
    - adj_list: a list of lists
        adj[x][y], where x represents a node, y represents another node and its corresponding weight to getting there.
    - dp: a list of int
        each index represents the maximum distance to each node
    - visited: a list of booleans
        each index represents whether or not a node has been visited before
    - pred: a list of int
        each int represents the index of what node comes before it on the path
    - i: an int
        represents which node we are currently at

    Worst-Case Time Complexity
    O(N), where N is the number of nodes we need to check
    
    Worst-Case Auxiliary-Space Complexity
    O(1), does not take much space
    """
    if visited[i] == True:
        return
    else:
        visited[i] == True
    
    # Check the neighbours
    # Note j[0] represents the node that is a neighbour, where as j[1] represents the weight of the node
    for j in adj_list[i]:
        if visited[j[0]] == False:
            dfs(adj_list, dp, visited, pred, j[0])
    # Once recursion hits bottom
        if dp[j[0]]+j[1] > dp[i]:
            pred[i] = j[0]
        dp[i] = max(dp[i], dp[j[0]]+j[1])


def find_max_index(arry):
    """
    Similiar to find_max, but instead of returning the max value, it instead returns the index of the max value

    Parameters:
    - arry: an array
        the array we want to look through, to find the index of the max value

    Output:
    Returns the index of the maximum value from an array

    Worst-Case Time Complexity
    O(N), where N is the number of items in the array
    
    Worst-Case Auxiliary-Space Complexity
    O(1), does not take up much space
    """
    max_value = 0
    index = 0
    for i in range(0,len(arry)):
        if arry[i] > max_value:
            max_value = arry[i]
            index = i
    return index