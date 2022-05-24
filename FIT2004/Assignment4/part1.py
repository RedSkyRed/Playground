def allocate(preferences, sysadmins_per_night, max_unwanted_shifts, min_shifts):
    allocation = None
    n = 30
    total_required_shifts = n*sys_admins_per_night
    total_admins = len(preferences[0])
    target = 2+total_admins+1+n+1
    unwanted_node = 2+total_admins


    # Quick check to see if there are enough shifts to go around
    if (total_required_shifts-(min_shifts*total_admins)) < 0:
        return allocation

    
    flow_graph = [None]*(target)

    # Filling up the first row
    flow_graph[0] = [[1, total_required_shifts-(min_shifts*total_admins)]]
        
    #  Filling in admins preference.    
    for j in range(total_admins):

        # Still filling in the first row
        flow_graph[0].append([j+2, min_shifts])

        # Filling the second row
        if flow_graph[1] == None:
            flow_graph[1] = [[j, n]]
        else:
            flow_graph[1].append([j, n])
        
        # Filling in each admin row
        flow_graph[j+2] = [[2+total_admins+1, max_unwanted_shifts]]
        for k in preferences[j]:
            if k == 1:
                if flow_graph[j+2] == None:
                    flow_graph[j+2] == [[3+total_admins+j,1]]
                else:
                    flow_graph[j+2].append([3+total_admins+j,1])

    # Filling out unwanted preferences to days.
    for i in range(n):
        if flow_graph[unwanted_node] == None:
            flow_graph[unwanted_node] = [[2+total_admins+1+i, 1]]
        else:
            flow_graph[unwanted_node].append([2+total_admins+1+i, 1])
            
        # Filling out each day to target variable
        flow_graph[2+total_admins+1+i] = [[target-1, sys_admins_per_night]]

    # if FordFulkerson(flow_graph, 0, 10) == total_required_shifts:
    #     # Needs to be modified but this is the basic idea
    #     allocation = flow_graph
    return allocation

def BFS(graph, source, target, parent) :
    visted = [False]*len(graph)
    queue = []
    queue.append(source)
    visted[source] = True

    while queue:
        cur_index = queue.pop(0)
        for i in graph[cur_index]:
            adj_index = i[0]
            if visted[adj_index] == False:
                queue.append(adj_index)
                visted[adj_index] = True
                parent[adj_index] = cur_index
                if cur_index == target:
                    return True
    return False

def FordFulkerson(graph, source, sink):
    parent = [-1]*len(graph)


    return None




preferences =  [[0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
                [0, 1, 1, 1, 0, 1, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
                [0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
                [1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                [0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0]]
min_shifts = 5
max_unwanted_shifts = 10
sys_admins_per_night = 6

res = allocate(preferences, sys_admins_per_night, max_unwanted_shifts, min_shifts)
print(res)

print(len(preferences))