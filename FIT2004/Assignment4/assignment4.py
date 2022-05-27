# Part 1
def allocate(preferences, sysadmins_per_night, max_unwanted_shifts, min_shifts):
    """
    Takes as an input a large list of preferences, for which admins would want to work on which nights, as well
    as a few other contstraints and then pushes out a list of lists, which allocates which admins to work on which days.
    
    In order to solve this combinatorial problem, I actually used a linked list, to create a flow graph.
    I then solved this flow graph using Ford-Fulkermon's Algorithm. 

    If my max_flow was equal to the total required shifts, then it meant that there was an allocation that satisfied
    all my constraints and I just then needed to convert my linked list flow graph into a allocation spreadsheet.
    The reason I opted for a linked list as opposed to a simple 2D graph, where my h x w, would be equal to the number of
    nodes is that I thought it would take too much space.

    Parameters:
    - preferences: a list of lists
        A grid that has both the days and which admins want to work on those days. Preferences[i][j], where is is
        the day and j is the admin who can work on that day. A 0 represents that they don't prefer to work on that day
        while a 1 represents, that they do
    - sysadmins_per_night: int
        The required amount of admins to work each night
    - max_unwanted_shifts: int
        The max number of shifts that can be assigned to an admin, given thier preferences
    - min_shifts: int
        The minimum amount of shifts that should be given to each admin

    Output:
    Returns a list of list. Allocation[i][j] where i represents the day, and j represents an admins willingness to work on that day

    Worst-Case Time Complexity
    O(N^2) Where N is the number of nights we have to roster for
    
    For visual purposes, here is a link to the flow graph created in this file:
    https://lucid.app/lucidchart/4924cf67-8be3-4665-9d3a-3e62ff54809d/edit?viewport_loc=-88%2C-16%2C2219%2C1065%2C0_0&invitationId=inv_60503043-e286-40e6-b856-80c859726e5f#
    """
    allocation = None
    # Number of days
    n = 30
    total_required_shifts = n * sysadmins_per_night
    total_admins = len(preferences[0])
    # The sink/target value, where all the flow will head towards.
    target = 2+total_admins*2+n+1

    # Quick check to see if there are enough shifts to go around
    if (total_required_shifts-(min_shifts*total_admins)) < 0:
        return allocation

    flow_graph = [None]*(target)

    # Filling up the first row. This is my (s)
    add_node(flow_graph, 0, 1, total_required_shifts-(min_shifts*total_admins))
    # Reversed for residual
    add_node(flow_graph, 1, 0, 0)
 
    for j in range(total_admins):

        # Filing in the connection between the starting node and the admins.
        # Making sure that each admin gets the minimum amount of shifts they want.
        add_node(flow_graph, 0, j+2, min_shifts)
        # Reversed for residual
        add_node(flow_graph, j+2, 0, 0)

        # Filling in the second row. This is the spare jobs that can be assigned to any admin, but need to be filled.
        add_node(flow_graph, 1, j+2, n)
        # Reversed for residual
        add_node(flow_graph, j+2, 1, 0)
        
        # Any jobs that the admins don't want, spills over to the admins unwanted shifts.
        add_node(flow_graph, j+2, total_admins+ j + 2, max_unwanted_shifts)
        # Reversed for residual
        add_node(flow_graph, total_admins + j + 2, j+2, 0)

    # Converting the preferences list, into admin nodes that connect to day nodes.
    for i in range(n):
        for k in range(len(preferences[i])):
            if preferences[i][k] == 1:
                add_node(flow_graph, k+2, 2+total_admins*2+i, 1)
                # Reversed for residual
                add_node(flow_graph, 2+total_admins*2+i, k+2, 0)
            else:
                # Unwanted admin nodes to each day node
                add_node(flow_graph, 2+total_admins+k, 2+total_admins*2+i, 1)
                # Reversed for residual
                add_node(flow_graph, 2+total_admins*2+i, 2+total_admins+k, 0)
            
        # Filling out each day to targe/sink end of our flow graph
        add_node(flow_graph, 2+total_admins*2+i, target-1, sysadmins_per_night)
        # Reversed for residual
        add_node(flow_graph, target-1, 2+total_admins*2+i, 0)

    allocation = FordFulkerson(flow_graph, 0, target-1, n, sysadmins_per_night, total_admins)
    return allocation

def add_node(graph, node, other_node, weight):
    """
    Very simple function that adds a node to a linked list graph.

    Parameters:
    - graph: list of lists
    A list of list that represents the nodes, and thier weight to one another.
    - node: int
    The node we want to connect to another node
    - other_node: int
    The other node we want to connect too
    - weight: int
    The weight of the relationship between the two nodes

    Worst-Case Time Complexity
    O(1)
    """

    if graph[node] == None:
        graph[node] = [[other_node, weight]]
    else:
        graph[node].append([other_node, weight])

def BFS(graph, s, t, parent):
    """
    Breadth First Search. An algorithm that searches through a graph until it can find the
    target node.

    Parameters:
    - graph: list of lists
    An adjacency list, that describes each nodes relationship and weight towards one another
    - s: int
    The starting node
    - t: int
    The target node we want to end at
    - parent: list of int
    A list used to hold the index of each node's parent

    Output:
    Returns a boolean, depending or not a path can be found to the target path.

    Worst-Case Time Complexity
    O(V + E) Where V is the number of Nodes and E is the number of edges
    """

    visted = [False]*len(graph)
    queue = []
    queue.append(s)
    visted[s] = True

    # Goes through all nodes that can be reached from the starting node
    while queue:
        cur_index = queue.pop(0)
        
        for i in graph[cur_index]:
            adj_index = i[0]
            if visted[adj_index] == False and i[1] > 0:
                queue.append(adj_index)
                visted[adj_index] = True
                parent[adj_index] = cur_index
                if adj_index == t:
                    return True
    return False

def FordFulkerson(graph, source, sink, n, sysadmin_per_night, total_admins):
    """
    Ford-Fulkerson Algorithm, used for finding the max flow in a direct acyclical graph.
    This algorithm was heavily inspired by this website:
    https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/

    Parameters:
    - graph: list of lists
    A list of list that represents the nodes, and thier weight to one another.
    - source: int
    The node we want to start from
    - sink: int
    The node we want to finish on
    - n: int
    The total number of nights we want to allocate
    - sysadmin_per_night: int
    The total number of admins we need per night
    - total_admins: int
    A derived number that tells us the total number of admins we have to roster on.

    Worst-Case Time Complexity
    O(N^2) Where N is the number of nights.

    References:
    GeeksforGeeks. (2013). Ford-Fulkerson Algorithm for Maximum Flow Problem - GeeksforGeeks. 
    [online] Available at: https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/ [Accessed 27 May 2022].
    """
    allocation = [[0]*total_admins]

    for i in range(n-1):
        allocation.append([0]*total_admins)

    parent = [-1]*len(graph)

    max_flow = 0

    # Runs until there are no more paths available
    while BFS(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while (s != source):
            # Index finder for the linked list
            ind = None
            for i in range(len(graph[parent[s]])):
                if graph[parent[s]][i][0] == s:
                    ind = i 
            path_flow = min(path_flow, graph[parent[s]][ind][1])
            s = parent[s]
        
        max_flow += path_flow

        v = sink
        while (v != source):
            u = parent[v]

            # Because we used an adjacency matrix, we need to actually find the index of the variable we want
            ind_v = None
            for i in range(len(graph[u])):
                if graph[u][i][0] == v:
                    ind_v = i 
            graph[u][ind_v][1] -= path_flow
            
            # Because we used an adjacency matrix, we need to actually find the index of the variable we want
            ind_u = None
            for i in range(len(graph[v])):
                if graph[v][i][0] == u:
                    ind_u = i 
            graph[v][ind_u][1] += path_flow
            
            v = parent[v]

    # Filling out the allocations list of lists
    if (max_flow == sysadmin_per_night * n):
        for i in range(total_admins):
            for j in graph[i+2]:
                if (j[0] != total_admins+i+2) and j[1] == 0:
                    index = j[0] - (total_admins*2 + 2)
                    allocation[index][i] = 1
            for k in graph[i+2+total_admins]:
                if (k[0] != i+2) and k[1] == 0:
                    index = k[0] - (total_admins*2 + 2)
                    allocation[index][i] = 1
    else:
        allocation = None
    return allocation

# Part 2

class EventsTrie:
    """
    A class that makes a trie, that stores all the suffixes of a list of words when intialised.
    Useful for finding the longest word with a minimum amount of reoccurrences.
    Also useful for fighting Master X.
    """
    def __init__(self, timelines):
        """
        Intialises EventsTrie, by pushing all of our words into a suffix trie.

        Parameters:
        - timelines: a list of str
        A list of words, in which each letter of each word represents an event that happens in a sequence

        Worst-Case Time Complexity
        O(NM^2) WHere N is the number of timelines in timelines and M is the number of events in the longest timeline
        """
        self.timelines = timelines
        self.starting_node = Node(0,1)
        # A list where each index represents the number of occurences, and each value is the longest timeline with that number of occurences
        self.longest_timelines = [None]*(len(timelines)+1)

        timeline_no = 0

        # For every word in our timeline
        for i in self.timelines:
            timeline_no += 1
            suffix_queue = []
            letter_queue = []
            # Add to our suffix queue smaller and smaller words
            for k in range(len(i)):
                suffix_queue.append(i[k:])
            # While thier are suffixs still left in our queue
            while suffix_queue:
                suffix = suffix_queue.pop(0)
                # Add all the leters of the suffix to the queue
                for j in list(suffix):
                    letter_queue.append(j)
                # Reset the queue to the top
                curr_node = self.starting_node
                # Go through all the letters of the suffix
                while letter_queue:
                    curr_letter = letter_queue.pop(0)\
                    # If a child node does already exist
                    if curr_node.child_exists(curr_letter):
                        curr_node = curr_node.return_child(curr_letter)
                        if not curr_node.check_visited(timeline_no):
                            curr_node.chain_increment()
                            curr_node.new_visit(timeline_no)
                            # If this particular combination of timelines is the biggest, add it to our longest timeslines list.
                            if self.longest_timelines[curr_node.return_chain()] == None:
                                self.longest_timelines[curr_node.return_chain()] = suffix[:curr_node.return_depth()] 
                            elif len(self.longest_timelines[curr_node.return_chain()]) < curr_node.return_depth():
                                self.longest_timelines[curr_node.return_chain()] = suffix[:curr_node.return_depth()]                            
                    # If a child node does not exist
                    else:
                        new_node = Node(curr_letter, timeline_no)
                        new_node.set_depth(curr_node.return_depth()+1)
                        curr_node.add_child(new_node)
                        curr_node = curr_node.return_child(curr_letter)
                    # If this is the last letter in the queue
                    if not letter_queue:
                        if self.longest_timelines[curr_node.return_chain()] == None:
                            self.longest_timelines[curr_node.return_chain()] = suffix[:curr_node.return_depth()] 
                        elif len(self.longest_timelines[curr_node.return_chain()]) < curr_node.return_depth():
                             self.longest_timelines[curr_node.return_chain()] = suffix
                        curr_node.add_child(Node('$', timeline_no))

    def getLongestChain(self, noccurence):
        """
        Very simple function that takes a number of occurences and returns the longest timeline with
        those number of occurrences. Made simple by it being recorded when the trie was intialized

        Parameters:
        - noccurence: int
        The number of occurences we want to find the longest timeline for.

        Output:
        Returns the longest word with that number of occurrences or more.

        Worst-Case Time Complexity
        O(1), as this is a matter of looking up an index
        """
        return self.longest_timelines[noccurence]


class Node:
    """
    A class used to help keep track of our graph and store vital information
    """
    def __init__(self, data, timeline):
        """
        Intialises the Node class

        Parameters:
        - data: str
        A letter that the node stores
        - timeline: int
        Used to help keep track of which timelines this node has been apart of.

        Worst-Case Time Complexity
        O(1), just intializing variables
        """
        self.data = data
        self.timeline = [0]
        self.depth = 0
        self.chain = 1
        self.children = []

        self.timeline.append(timeline)

    def check_visited(self, tm_line):
        """
        Checks if a node has already been visited by someone in that timeline.

        Parameters:
        - tm_line: int
        The timeline that we want to check

        Output:
        Returns a boolean, with True if the node has already been visited and False if it hasn't

        Worst-Case Time Complexity
        O(T), where T is the number of timelines
        """
        already_visited = False
        for t in range(len(self.timeline)):
            if self.timeline[t] == tm_line:
               already_visited = True
        return already_visited

    def new_visit(self, timeline_no):
        """
        Adds a timeline to the list of its visited ones

        Parameters:
        - timeline_no: int
        The timeline that we want to add to our visited for the node

        Worst-Case Time Complexity
        O(1)
        """
        self.timeline.append(timeline_no)

    def return_data(self):
        """
        Returns the data or charachter that this node holds

        Output:
        Returns a str

        Worst-Case Time Complexity
        O(1)
        """
        return self.data

    def return_depth(self):
        """
        Returns the depth of the node from the source node

        Output:
        Returns a int which is its depth from the source node

        Worst-Case Time Complexity
        O(1)
        """
        return self.depth

    def return_chain(self):
        """
        Returns the amount of timeslines that this node has been apart of

        Output:
        Returns an int, which represents the number of timelines

        Worst-Case Time Complexity
        O(1)
        """
        return self.chain

    def set_depth(self, n):
        """
        Sets the depth of the node from the source node

        Parameters:
        - n: an int
        The depth which we want to set

        Worst-Case Time Complexity
        O(1)
        """
        self.depth = n

    def chain_increment(self):
        """
        Increments the chain

        Worst-Case Time Complexity
        O(1)
        """
        self.chain += 1

    def child_exists(self, letter):
        """
        Checks whether or not a child node exists with the required letter

        Parameters:
        - letter: a str
        The string we want to check against the child nodes

        Output:
        Returns a boolean, which indicates whether or not a child node exists with the required letter

        Worst-Case Time Complexity
        O(C), where C is the number of children a node can have
        """
        for i in self.children:
            if letter == i.return_data():
                return True
        return False

    def return_child(self, letter):
        """
        Returns a child node, that holds the required letter

        Parameters:
        - letter: a str
        The string we want to check against the child nodes

        Output:
        Returns the node we are looking for

        Worst-Case Time Complexity
        O(C), where C is the number of children a node can have
        """
        for i in self.children:
            if letter == i.return_data():
                return i
        return None

    def add_child(self, node):
        """
        Adds a child node to this node

        Parameters:
        - node: a object
        The node we want this node to parent

        Worst-Case Time Complexity
        O(1)
        """
        self.children.append(node)
