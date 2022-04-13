class Heap:
    def __init__(self) -> None:
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapMinHeapNode(self, a, b):
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
    
                self.swapMinHeapNode(smallest, idx)
    
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
            self.swapMinHeapNode(i, (i - 1)//2 )
            i = (i - 1) // 2
 
    def isInMinHeap(self, v):
        if self.pos[v] < self.size:
            return True
        return False



class RoadGraph:
    def __init__(self,roads):
        self.num_of_locations = self.num_of_locations(roads)
        self.graph, self.r_graph = self.adj_list(roads)

    def adj_list(self, list):
        adj_list = [None] * self.num_of_locations
        r_adj_list = [None] * self.num_of_locations
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
        paths_distance, paths_pred = self.shortest_path(self.graph, start)
        r_paths_distance, r_paths_pred = self.shortest_path(self.r_graph, end)
        best_route = None
        best_chore = self.optimal_chore(chores_location, paths_distance, paths_pred, r_paths_distance, r_paths_pred)

        if best_chore != None:
            i = best_chore
            j = best_chore
            forward_route_list = []
            backward_route_list = []
            while paths_pred[i] != start:
                forward_route_list.append(paths_pred[i])
                i = paths_pred[i]
            while r_paths_pred[j] != end:
                backward_route_list.append(r_paths_pred[j])
                j = r_paths_pred[j]
            best_route = [start]
            while forward_route_list != []:
                best_route.append(forward_route_list.pop())
            best_route.append(best_chore)
            while backward_route_list != []:
                best_route.append(backward_route_list.pop(0))
            best_route.append(end)         
        return best_route


    def optimal_chore(self, chore_location, paths_distance, paths_pred, r_paths_distance, r_paths_pred):
        possible_chores = []
        best_chore = None
        best_chore_distance = None
        for i in chores_location:
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
        distance_list = [float('inf')]*self.num_of_locations
        pred_list = [None] * self.num_of_locations
        distance_list[start] = 0

        minHeap = Heap()

        for i in range(self.num_of_locations):
            minHeap.array.append(minHeap.newMinHeapNode(i, distance_list[i]))
            minHeap.pos.append(i)

        minHeap.decreaseKey(start, distance_list[start])
        minHeap.size = self.num_of_locations

        while minHeap.isEmpty() == False:
            popped_node =minHeap.extractMin()
            u = popped_node[0]

        # Here i is the location of the node, i[0] is the node that is being traveled to
        #  and i[1] is the weight of that node
            if graph[u] != None:
                for i in graph[u]:
                    v = i[0]
                    w = i[1]
                    if minHeap.isInMinHeap(v) and w + distance_list[u] < distance_list[v]:
                        distance_list[v] = w + distance_list[u]
                        pred_list[v] = u
                        minHeap.decreaseKey(v, distance_list[v])
        return distance_list, pred_list

roads = [(0,1,4), (0,3,2), (0,2,3), (2,3,2),(3,0,3)]
roads2 = [(0, 1 ,4), (1, 2 ,2), (2, 3 ,3), (3, 4 ,1), (1, 5 ,2),
(5, 6 ,5), (6, 3 ,2), (6, 4 ,3), (1, 7 ,4), (7, 8 ,2),
(8, 7 ,2), (7, 3 ,2), (8, 0 ,11)]
roads3 = [(0, 1 ,4), (1, 2 ,2), (2, 3 ,3), (3, 4 ,1), (1, 5 ,2),
(5, 6 ,5), (6, 3 ,2), (6, 4 ,3), (1, 7 ,4), (7, 8 ,2),
(8, 7 ,2), (7, 3 ,2), (8, 0 ,11), (4, 3, 1), (4, 8, 10)]

mysecondgraph = RoadGraph(roads3)

start = 7
end = 4
chores_location = [5,6,8]

print(mysecondgraph.routing(start, end, chores_location))