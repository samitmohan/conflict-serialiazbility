# simple idea of cycle prediction + top sort.

from collections import defaultdict

class Graph():
    def __init__(self, vertices) -> None:
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isCyclic(self, v, visited, Stack):
        visited[v], Stack[v] = True, True # if any neigh is visited & in stack : cyclic
        for neigh in self.graph[v]:
            if visited[neigh] == False:
                # haven't visited yet, check for before if it alr consists of cycle
                if self.isCyclic(neigh, visited, Stack): return True
            elif Stack[neigh] == True: return True
        Stack[v] = False
        return False


    def iC(self):
        if self.V == 0: return False # edge case : graph has no vertices
        # initial setup
        visited = [False] * self.V
        Stack = [False] * self.V
        for node in range(self.V):
            if visited[node] == False:
                if self.isCyclic(node, visited, Stack) == True: return True
        return False

    # top sort
    def topSortAlgo(self, v, visited, stack):
        visited[v] = True
        for adj in self.graph[v]:
            if visited[adj] == False:
                self.topSortAlgo(adj, visited, stack)
            # curr vertex to stack (indegree 0 after done)
        stack.insert(0, v) # only add vertex after dealing with the neighbours

    def topSort(self):
        if self.V == 0: return False # edge case : graph has no vertices
        visited, stack = [False] * self.V, []
        for i in range(self.V):
            if visited[i] == False:
                self.topSortAlgo(i, visited, stack)
        return stack
