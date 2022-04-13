from queue import PriorityQueue


class RoadGraph:
    def __init__(self,roads):
        self.num_of_locations = self.num_of_locations(roads)
        self.graph = self.adj_list(roads)
        self.reverse_graph = self.reverse_adj_list(roads)

    
    def adj_list(self, list):
        adj_list = [None] * self.num_of_locations
        while list != []:
            current = roads.pop()
            if adj_list[current[0]] != None:
                adj_list[current[0]].extend([[current[1],current[2]]])
            else:
                adj_list[current[0]] = [[current[1],current[2]]]
        return adj_list

# Might be a redundant function, could modify the above one.
    def reverse_adj_list(self, list):
        adj_list = [None] * self.num_of_locations
        while list != []:
            current = roads.pop()
            if adj_list[current[0]] != None:
                adj_list[current[1]].extend([[current[0],current[2]]])
            else:
                adj_list[current[1]] = [[current[0],current[2]]]
        return adj_list

    def num_of_locations(self, list):
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
        paths = self.shortest_paths(self.adj_list, start)
        reverse_paths = self.shortest_paths(self.reverse_adj_list, end)

    def shortest_path(self, adj_list, start):
        distance_list = [float('inf')]*self.num_of_locations
        pred_list = [0] * self.num_of_locations
        # distance_list[start] = 0
        # Q = PriorityQueue
        # while Q != []:
        #     u = Q.pop_min()
        #     for i in 
        return distance_list, pred_list

roads = [(0,1,4), (0,3,2), (0,2,3), (2,3,2),(3,0,3)]
mygraph = RoadGraph(roads)

start = 0
end = 1
chores_location = [2,3]