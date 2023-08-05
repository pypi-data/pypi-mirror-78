class NQueens:
    """
    obj = NQueens()
    obj.solveNQ(5)
    """
    @staticmethod
    def printSolution(board: list, N: int) -> None:
        """
        :param board: List of list of integers signifying the chess board
        :param N: Size of the board

        Printing the solution

        :return: None (Void)
        """

        for i in range(N):
            for j in range(N):
                print(board[i][j], end=" ")
            print()

    @staticmethod
    def isSafe(board: list, row: int, col: int, N: int) -> bool:
        """
        :param board: List of list of integers signifying the chess board
        :param row: Current row
        :param col: Current column
        :param N: Size of the board

        A utility function to check if a queen can be placed on board[row][col]. Note that this
        function is called when "col" queens are already placed in columns from 0 to col - 1.
        So we need to check only left side for attacking queens.

        :return: Returns true if the current configuration is safe otherwise false
        """
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, N, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def solveNQUtil(self, board: list, col: int, N: int) -> bool:
        """
        :param board: List of list of integers signifying the chess board
        :param col: Current column
        :param N: Size of the board

        Utility function for solving the problem

        :return: True if the queen can be placed or not
        """
        if col >= N:
            return True
        for i in range(N):
            if self.isSafe(board, i, col, N):
                board[i][col] = 1
                if self.solveNQUtil(board, col + 1, N):
                    return True
                board[i][col] = 0
        return False

    def solveNQ(self, N) -> bool:
        """
        :param N: Size of the board

        This function solves the N Queen problem using Backtracking.
        It mainly uses solveNQUtil() to solve the problem. It returns false if queens cannot be placed,
        otherwise return true and placement of queens in the form of 1s.
        note that there may be more than one solutions, this function prints one of the feasible solutions.

        :return: True if the queens can be placed in non attacking positions
        """
        board = [[0 for _ in range(N)] for __ in range(N)]
        if not self.solveNQUtil(board, 0, N):
            print("Solution does not exist")
            return False
        self.printSolution(board, N)
        return True
