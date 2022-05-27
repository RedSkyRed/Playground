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
