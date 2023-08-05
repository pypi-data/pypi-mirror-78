class MColouringProblem:
    """
    obj = MColouringProblem(4)
    obj.graph = [[0, 1, 1, 1],
                 [1, 0, 1, 0],
                 [1, 1, 0, 1],
                 [1, 0, 1, 0]]
    obj.graphColouring(3)
    """
    def __init__(self, vertices: int) -> None:
        """
        :param vertices: Number of vertices

        Initializing the adjacency matrix

        :return: None (Void)
        """
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for __ in range(vertices)]

    def isSafe(self, v: int, colour: list, c: int) -> bool:
        """
        :param v: Vertices
        :param colour: List of colours
        :param c: Colour

        A utility function to check if the current color assignment
        is safe for vertex v

        :return: Returns true if its safe to assign the specified colour
        """
        for i in range(self.V):
            if self.graph[v][i] == 1 and colour[i] == c:
                return False
        return True

    def graphColourUtil(self, m: int, colour: list, v: int) -> bool:
        """
        :param m: Number of colours
        :param colour: List of colours
        :param v: Vertices

        A recursive utility function to solve m coloring  problem

        :return: Returns boolean if we can color the graph
        """
        if v == self.V:
            return True
        for c in range(1, m + 1):
            if self.isSafe(v, colour, c):
                colour[v] = c
                if self.graphColourUtil(m, colour, v + 1):
                    return True
                colour[v] = 0

    def graphColouring(self, m: int) -> bool:
        """
        :param m: Number of colours

        Checks whether the given graph can be coloured with m colors

        :return: Returns a boolean whether the given graph can be coloured with m colors
        """
        colour = [0] * self.V
        if self.graphColourUtil(m, colour, 0) is None:
            return False
        print("Solution exist and Following are the assigned colours:")
        for c in colour:
            print(c, end=' ')
        print()
        return True
