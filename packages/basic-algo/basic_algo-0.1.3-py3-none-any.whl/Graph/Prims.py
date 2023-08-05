from sys import maxsize


class Prims:
    """
    Create Graph using Kruskals Graph and find Minimum Spanning Tree.
    g = Prims(5)
    g.addEdge(0, 1, 2)
    g.addEdge(0, 3, 6)
    g.addEdge(1, 2, 3)
    g.addEdge(1, 3, 8)
    g.addEdge(1, 4, 5)
    g.addEdge(2, 4, 7)
    g.addEdge(3, 4, 9)
    g.primMST(0)
    """
    def __init__(self, vertices: int) -> None:
        """
        :param vertices: Number of vertices

        Initialising Graph

        :return None (Void)
        """
        try:
            assert isinstance(vertices, int)
        except AssertionError as _:
            print("vertices should be int.")
            raise
        self.V = vertices
        self.graph = []
        for i in range(self.V):
            self.graph.append([])

    def addEdge(self, u: int, v: int, w: int) -> None:
        """
        :param u: uth node
        :param v: child of u
        :param w: weight of edge between u and v

        Function to add an edge to graph

        :return: None (Void)
        """
        try:
            assert isinstance(u, int)
        except AssertionError as _:
            print("u should be int.")
            raise
        try:
            assert isinstance(v, int)
        except AssertionError as _:
            print("v should be int.")
            raise
        try:
            assert isinstance(w, int)
        except AssertionError as _:
            print("w should be int.")
            raise
        self.graph[u].append([v, w])
        self.graph[v].append([u, w])

    def minKey(self, key: list, mstSet: list) -> int:
        """
        :param key: Key values used to pick minimum weight edge in cut
        :param mstSet: list of nodes already included.

        A utility function to find the vertex with minimum distance value, from the set of vertices not yet included in
        shortest path tree

        :return: Minimum distance value
        """
        try:
            assert isinstance(key, list)
        except AssertionError as _:
            print("key should be list")
            raise
        try:
            assert isinstance(mstSet, list)
        except AssertionError as _:
            print("mstSet should be list.")
            raise
        minimum = maxsize
        min_index = -1
        for v in range(self.V):
            if key[v] < minimum and not mstSet[v]:
                minimum = key[v]
                min_index = v
        return min_index

    def primMST(self, src: int) -> None:
        """
        We use a boolean array mstSet[] to represent the set of vertices included in MST. If a value mstSet[v] is true,
        then vertex v is included in MST, otherwise not. Array key[] is used to store key values of all vertices.
        Another array parent[] to store indexes of parent nodes in MST. The parent array is the output array which is
        used to show the constructed MST.

        :return: None (Void)
        """
        try:
            assert isinstance(src, int)
        except AssertionError as _:
            print("src should be int.")
            raise
        key = [maxsize] * self.V
        parent = [-1] * self.V
        key[src] = 0
        mstSet = [False] * self.V
        parent[src] = -1
        for _ in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(len(self.graph[u])):
                if self.graph[u][v][1] < key[self.graph[u][v][0]] and not mstSet[self.graph[u][v][0]]:
                    key[self.graph[u][v][0]] = self.graph[u][v][1]
                    parent[self.graph[u][v][0]] = u
        print("Edge\tWeight")
        for i in range(self.V):
            if i != src:
                print(parent[i], "-", i, "\t", key[i])
