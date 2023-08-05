class Kruskals:
    """
    Create Graph using Kruskals Graph and find Minimum Spanning Tree.
    g = Kruskals(4)
    g.addEdge(0, 1, 10)
    g.addEdge(0, 2, 6)
    g.addEdge(0, 3, 5)
    g.addEdge(1, 3, 15)
    g.addEdge(2, 3, 4)

    result = g.KruskalMST()
    total_cost = 0
    for i in result:
        print(i[0], " -- ", i[1], " = ", i[2])
        total_cost += i[2]

    print("Total Cost: ", total_cost)

    MST:
          10
        0 -- 1
      5 |
        |
        3 -- 2
          4
    """
    def __init__(self, vertices: int) -> None:
        """
        :param vertices: Number of vertices

        Initialising Graph

        :return: None (Void)
        """
        self.V = vertices
        self.graph = []

    def addEdge(self, u: int, v: int, w: int) -> None:
        """
        :param u: uth node
        :param v: child of u
        :param w: weight of edge between u and v

        function to add an edge to graph

        :return: None (Void)
        """
        self.graph.append([u, v, w])

    def find(self, parent: list, i: int) -> int:
        """
        :param parent: list of parents of nodes
        :param i: element whose parent is to be found

        A utility function to find set of an element i (uses path compression technique)

        :return: Parent of i
        """
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent: list, rank: list, x: int, y: int) -> None:
        """
        :param parent: list of parents of nodes
        :param rank: Rank of nodes for DSU
        :param x: parent of u
        :param y: parent of v

        A function that does union of two sets of x and y (uses union by rank)

        :return: None (Void)
        """
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def KruskalMST(self) -> list:
        """
        Below are the steps for finding MST using Kruskal’s algorithm
            1. Sort all the edges in non-decreasing order of their weight.
            2. Pick the smallest edge. Check if it forms a cycle with the spanning tree formed so far. If cycle is not
               formed, include this edge. Else, discard it.
            3. Repeat step#2 until there are (V-1) edges in the spanning tree.
        The step #2 uses Union-Find algorithm to detect cycle.
        The algorithm is a Greedy Algorithm. The Greedy Choice is to pick the smallest weight edge that does not cause
        a cycle in the MST constructed so far.

        :return: Minimum Spanning Tree
        """
        result = []
        i = 0
        e = 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        return result
