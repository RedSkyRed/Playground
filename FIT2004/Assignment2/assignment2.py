# Part 1
def ideal_place(relevant):
    """
    Returns a location that is the minimum amount of combined distance to any relevant point.

    Parameters:
    - relevant: array of int
        The locations on our grid, that we want the minimum distance too

    Output:
    Returns a single location, that has a minimum combined distance from any relevant point.

    Worst-Case Time Complexity
    O(N), where N is the number of relevant points
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of relevant points
    """

    desired_place = [median_relevant_on_axis(relevant, 0),median_relevant_on_axis(relevant, 1)]
    return desired_place

def median_relevant_on_axis(relevant, axis_index):
    """
    Returns the median value out of the relevant points, on a particular axis

    Parameters:
    - relevant: array of int
        The locations on our grid, that we want the minimum distance too
    - axis_index
        The index of the axis in the relevant points that we want to find. x = 0, y = 1.

    Output:
    Returns a the median value from a particular index, in an array.

    Worst-Case Time Complexity
    O(N), where N is the number of relevant points
    
    Worst-Case Auxiliary-Space Complexity
    O(N), where N is the number of relevant points
    """

    length_of_arry = len(relevant)
    median_index = length_of_arry//2
    arry_on_axis = []

    # This is adding all of the values from a particular index, into an array.
    # For example, we would put all the y-coordinates into the arry_on_axis
    for i in range(0, length_of_arry):
        arry_on_axis.append(relevant[i][axis_index])
    
    # We then run quick select on that array
    desired_value = quick_select(arry_on_axis, 0, length_of_arry-1, median_index)
    return desired_value

def quick_select(arry, lo, hi, k):
    """
    Quickly selects the kth element from a list, using partitioning to reduce the complexity

    Parameters:
    - arry: an array of int 
        A list of integers we want to quickly select from
    - lo: int
        The lower bound index for what we want to search
    - hi: int
        The higher bound index for what we want to search
    - k: int
        The index of the element we want to find

    Output:
    Returns the kth element, from an array

    Worst-Case Time Complexity
    O(N), where N is the number of items in the array
    
    Worst-Case Auxiliary-Space Complexity
    O(logN), where N is the number of items in the array
    """

    # If the array only has size of 1 we want to return that element
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

def median_of_medians(arry):
    """
    Used to reduce the worst time complexity. Returns a rough median of medians, that allows our quickselect to run in O(N) worst time complexity

    Parameters:
    - arry: array of int
        An array of integers we want to find the rough median for

    Output:
    Returns a median value that can be used as an effective pivot

    Worst-Case Time Complexity
    O(N), where N is the number of items in the array
    
    Worst-Case Auxiliary-Space Complexity
    O(logN), where N is the number of items in the array
    """

    n = len(arry)
    if n <= 5:
        return insertion_sort_median(arry)
    medians = []
    for i in range(0,n//5):
        medians.append(insertion_sort_median(arry[5*i:5*i+5]))
    return quick_select(medians, 0, len(medians), len(medians)//2)    

def insertion_sort_median(arry):
    """
    Basic sorting algorithm, for smaller lists. Returns the median once it is found.

    Parameters:
    - arry: an array of int
        The list to be sorted

    Output:
    Returns the median in a sorted list.

    Worst-Case Time Complexity
    O(N^2), where N is the number of items in the array
    
    Worst-Case Auxiliary-Space Complexity
    O(1), it is in an in place algorithm
    """

    arry_length = len(arry)
    for i in range (1, arry_length):
        pointer = arry[i]
        j = i-1
        while j >= 0 and pointer < arry[j]:
            arry[j + 1] = arry[j]
            j -= 1
        arry[j + 1] = pointer
    return arry[arry_length//2]

def partition(arry, lo, hi, pivot):
    """
    Splits up the algorithm, and partitions them into two sides, based on a pivot.

    Parameters:
    - arry: an array of int
        The list to be partitioned
    - lo: int
        The lower bound index for what we want to partition
    - hi: int
        The higher bound index for what we want to partition
    - pivot: int
        The item we want to partition the list around.

    Output:
    Returns the mid point, after we have partitioned.

    Worst-Case Time Complexity
    O(N), where N is the number of elements in the array
    
    Worst-Case Auxiliary-Space Complexity
    O(1), an in place algorithm
    """

    # Basically finding the pivot in the array, and places it at the very end of our list
    for i in range(lo, hi):
        if arry[i] == pivot:
            swap(arry, hi, i)
            break
 
    v = arry[hi]
    i = lo
    for j in range(lo, hi):
        if (arry[j] <= v):
            swap(arry, i, j)
            i += 1
    # Place back our pivot, into the middle where it belongs
    swap(arry, i, hi)
    return i

def swap(arry, i, j):
    """
    Swaps two elements in an array

    Parameters:
    - arry: an array of int
        The array in which we want the items to be swapped in.
    - i: int
        The index for the first item we want swapped
    - j: int
        The index for the second item we want swapped

    Worst-Case Time Complexity
    O(1), runs in constant time
    
    Worst-Case Auxiliary-Space Complexity
    O(1), an in place algorithm
    """
    arry[i],arry[j] = arry[j],arry[i]

# --------------------------------------
# Part 2

class Heap:
    """
    Mehta.D (2022) Dijkstra's Algorithm for Adjacency List [Source Code] https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/
    The Heap Class used here was pulled from the above source

    A class that allows us to easily heapify and manage a heap. Particularly useful when wanting to implement a priority queue
    """

    def __init__(self) -> None:
        """
        Intializes the heap

        Worst-Case Time Complexity
        O(1), runs in constant time
        
        Worst-Case Auxiliary-Space Complexity
        O(1), an in place algorithm
        """

        self.array = []
        self.size = 0
        self.pos = []

    def newNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    def minHeapify(self, idx):
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
 
        if (left < self.size and
           self.array[left][1]
            < self.array[smallest][1]):
            smallest = left
 
        if (right < self.size and
           self.array[right][1]
            < self.array[smallest][1]):
            smallest = right    
            if smallest != idx:
            
                self.pos[self.array[smallest][0]] = idx
                self.pos[self.array[idx][0]] = smallest
    
                self.swapNode(smallest, idx)
    
                self.minHeapify(smallest)

    def extractMin(self):
 
        if self.isEmpty() == True:
            return
 
        root = self.array[0]
 
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
 
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
 
        self.size -= 1
        self.minHeapify(0)
 
        return root
 
    def isEmpty(self):
        return True if self.size == 0 else False
 
    def decreaseKey(self, v, dist):

        i = self.pos[v]

        self.array[i][1] = dist

        while (i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]):
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapNode(i, (i - 1)//2 )
            i = (i - 1) // 2
 
    def isInMinHeap(self, v):
        if self.pos[v] < self.size:
            return True
        return False



class RoadGraph:
    """
    A class that allows us to mangage and interact with roads. 
    """

    def __init__(self,roads):
        """
        Intializes the graph using an adjacency list

        Parameters:
        - roads: a list of tuples
            The roads that the graph will keep track off.

        Worst-Case Time Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        
        Worst-Case Auxiliary-Space Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        """

        self.num_of_locations = self.num_of_locations(roads)
        self.graph, self.r_graph = self.adj_list(roads)

    def adj_list(self, list):
        """
        Turns a list into an adjacency list.

        Parameters:
        - list: a list of tuples
            The roads that will fall into our adjacency list

        Output:
        Returns both an adjacency list, and the reverse adjacency list

        Worst-Case Time Complexity
        O(|E|), where E is the number of roads
        
        Worst-Case Auxiliary-Space Complexity
        O(|E|), where E is the number of roads
        """

        adj_list = [None] * self.num_of_locations
        r_adj_list = [None] * self.num_of_locations

        # This loop removes items from our list and places them into the adjacency and reverse adjacency list.
        while list != []:
            current = list.pop()
            if adj_list[current[0]] != None:
                adj_list[current[0]].extend([[current[1],current[2]]])
            else:
                adj_list[current[0]] = [[current[1],current[2]]]
            if r_adj_list[current[1]] != None:
                r_adj_list[current[1]].extend([[current[0],current[2]]])
            else:
                r_adj_list[current[1]] = [[current[0],current[2]]]
        return adj_list, r_adj_list

    def num_of_locations(self, list):
        """
        Iterates through the list of roads, and finds the total number of locations. 
        We assume that all locations are interconnected and thus can be reached by a road.

        Parameters:
        - list: a list of tuples
            All the roads

        Output:
        Returns the amount of locations present among all the roads.

        Worst-Case Time Complexity
        O(|E|), where E is the number of roads
        
        Worst-Case Auxiliary-Space Complexity
        O(1), in place.
        """

        max = 0
        if list != None:
            for i in range(len(list)):
                if list[i][0] > max:
                    max = list[i][0]
                elif list[i][1] > max:
                    max = list[i][1]
            max += 1
        return max
        
    def routing(self, start, end, chores_location):
        """
        Finds the best way to transverse through the roads, given that we want to do a chore on the way

        Parameters:
        - start: an int
            The starting location represented by an integer
        - end: an int
            The end location represented by an integer
        - chores_location
            An array of locations that have chores at them
        
        Output:
        We return an array with all the locations we should visit and what order we should vist them, if we want to go from
        start to end and visit a location with a chore.

        Worst-Case Time Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        
        Worst-Case Auxiliary-Space Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        """

        paths_distance, paths_pred = self.shortest_path(self.graph, start)
        r_paths_distance, r_paths_pred = self.shortest_path(self.r_graph, end)
        best_route = None
        
        # We check which chore can be reached by both the start and the end, and has the smallest combined distance from start to end
        best_chore = self.optimal_chore(chores_location, paths_distance, paths_pred, r_paths_distance, r_paths_pred)

        # Now that we have hopefully found the best chore to reach if it exists, we now need to backtrack and find how to get there.
        if best_chore != None:
            i = best_chore
            j = best_chore
            forward_route_list = []
            backward_route_list = []

            # We place our minimum route from the start to the chore into a list, by working through the predecessors list
            while paths_pred[i] != start:
                forward_route_list.append(paths_pred[i])
                i = paths_pred[i]

            # We place our minimum route from the end to the chore into a list, by working through the predecessors list
            while r_paths_pred[j] != end:
                backward_route_list.append(r_paths_pred[j])
                j = r_paths_pred[j]
            
            # We intialize our route
            best_route = [start]
            
            # We then want to add each element in the route from start too the chore to our list. 
            while forward_route_list != []:
                best_route.append(forward_route_list.pop())
            # Place our chore location into the route
            if best_chore != start:
                best_route.append(best_chore)
            # We then want to add each element in the route from end too the chore to our list. 
            while backward_route_list != []:
                best_route.append(backward_route_list.pop(0))
            # Add our end point to our list
            if end != best_chore:
                best_route.append(end)         
        return best_route


    def optimal_chore(self, chore_location, paths_distance, paths_pred, r_paths_distance, r_paths_pred):
        """
        Finds the chore with the smallest distance to both the start and end.

        Parameters:
        - chores_location
            An array of locations that have chores at them
        - paths_distance: an array of int
            An array with the minimum distance required to reach each location from the start point
        - paths_prede: an array of int
            An array with the predecessors of location, that allows a location to be reached by the start
        - r_paths_distance: an array of int
            An array with the minimum distance required to reach each location from the end point
        - paths_prede: an array of int
            An array with the predecessors of location, that allows a location to be reached by the end
        
        Output:
        We return the best chore, that can be reached by both the start and end, and has the smallest combined minimum distance.

        Worst-Case Time Complexity
        O(|C|), where C is the number of chores.
        
        Worst-Case Auxiliary-Space Complexity
        O(|C|), where C is the number of chores.
        """

        possible_chores = []
        best_chore = None
        best_chore_distance = None
        for i in chore_location:
            if paths_pred[i] != None and r_paths_pred[i] != None:
                possible_chores.append(i)
        if possible_chores != []:
            best_chore=possible_chores[0]
            best_chore_distance = paths_distance[best_chore] + r_paths_distance[best_chore]
            for i in possible_chores:
                if best_chore_distance > (paths_distance[i] + r_paths_distance[i]):
                    best_chore = i
                    best_chore_distance = paths_distance[i] + r_paths_distance[i]
        return best_chore

    def shortest_path(self, graph, start):
        """
        Finds the shortest path to each node in a graph

        Parameters:
        - graph: adjacency list
            An adjacency list with all the nodes, and how they connect to one another
        - start: an int
            Represents the starting location

        Worst-Case Time Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        
        Worst-Case Auxiliary-Space Complexity
        O(|V| + |E|), where V is the number of unique locations and E is the number of roads
        """

        distance_list = [float('inf')]*self.num_of_locations
        pred_list = [None] * self.num_of_locations
        distance_list[start] = 0

        # Intializing our heap. Acts as a priority queue.
        minHeap = Heap()

        # Filling up our heap with all the locations.
        for i in range(self.num_of_locations):
            minHeap.array.append(minHeap.newNode(i, distance_list[i]))
            minHeap.pos.append(i)

        minHeap.decreaseKey(start, distance_list[start])
        minHeap.size = self.num_of_locations

        # Each time we are going through the heap until it is empty, always removing the position with the smallest distance
        while minHeap.isEmpty() == False:
            new_node = minHeap.extractMin()
            # u represents where the road begins
            u = new_node[0]

            if graph[u] != None:
                for i in graph[u]:
                    # Here v and w are changed from i, for simplicities sake.
                    # v represents where the road leads too
                    # w represents the weight of said road
                    v = i[0]
                    w = i[1]
                    if minHeap.isInMinHeap(v) and w + distance_list[u] < distance_list[v]:
                        distance_list[v] = w + distance_list[u]
                        pred_list[v] = u
                        minHeap.decreaseKey(v, distance_list[v])
        return distance_list, pred_list