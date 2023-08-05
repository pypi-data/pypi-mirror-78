class SudokuSolving:
    """
    obj = SudokuSolving()
    grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    print(obj.solveSudoku(grid))
    """
    @staticmethod
    def printGrid(arr: list) -> None:
        """
        :param arr: Sudoku grid

        A Utility Function to print the Grid

        :return: None (Void)
        """
        for i in range(9):
            for j in range(9):
                print(arr[i][j], end=' ')
            print()

    @staticmethod
    def findEmptyLocation(arr: list, track: list) -> bool:
        """
        :param arr: Sudoku grid
        :param track: list variable to keep track of incrementation of Rows and Columns

        Function to Find the entry in the Grid that is still  not used
        Searches the grid to find an entry that is still unassigned.

        :return: If found, the reference parameters row, col will be set the location
        that is unassigned, and true is returned. If no unassigned entries
        remains, false is returned.
        """
        for row in range(9):
            for col in range(9):
                if arr[row][col] == 0:
                    track[0] = row
                    track[1] = col
                    return True
        return False

    @staticmethod
    def usedInRow(arr: list, row: int, num: int) -> bool:
        """
        :param arr: Sudoku grid
        :param row: Current row
        :param num: number to be matched

        Checks whether any assigned entry in the specified row matches the given number.

        :return: Returns a boolean which indicates whether any assigned entry in the specified row matches the given
                 number.
        """
        for i in range(9):
            if arr[row][i] == num:
                return True
        return False

    @staticmethod
    def usedInCol(arr: list, col: int, num: int) -> bool:
        """
        :param arr: Sudoku grid
        :param col: Current column
        :param num: Number ot be matched

        Checks whether any assigned entry in the specified column matches the given number.

        :return: Returns a boolean which indicates whether any assigned entry
        in the specified column matches the given number.
        """
        for i in range(9):
            if arr[i][col] == num:
                return True
        return False

    @staticmethod
    def usedInBox(arr: list, row: int, col: int, num: int) -> bool:
        """
        :param arr: Sudoku grid
        :param row: Current row
        :param col: Current column
        :param num: Number to be matched

        Checks whether any assigned entry in the specified 3x3 box matches the given number.

        :return: Returns a boolean which indicates whether any assigned entry
        in the specified 3x3 box matches the given number.
        """
        for i in range(3):
            for j in range(3):
                if arr[i + row][j + col] == num:
                    return True
        return False

    def checkLocationIsSafe(self, arr: list, row: int, col: int, num: int) -> bool:
        """
        :param arr: Sudoku grid
        :param row: Current row
        :param col: Current column
        :param num: Number ot be matched

        Checks whether it will be legal to assign num to the given row, col
        Returns a boolean which indicates whether it will be legal to assign
        num to the given row, col location.

        :return: Returns a boolean which indicates whether it will be legal to assign
        num to the given row, col location.
        """
        return not self.usedInRow(arr, row, num) and not self.usedInCol(arr, col, num) and not self.usedInBox(arr, row - row % 3, col - col % 3, num)

    def solveSudoku(self, arr: list) -> bool:
        """
        :param arr: Sudoku grid

        Takes a partially filled-in grid and attempts to assign values to
        all unassigned locations in such a way to meet the requirements
        for Sudoku solution (non-duplication across rows, columns, and boxes)

        :return: Returns a boolean whether it can be solved or not
        """
        track = [0, 0]
        if not self.findEmptyLocation(arr, track):
            self.printGrid(arr)
            return True
        row = track[0]
        col = track[1]
        for num in range(1, 10):
            if self.checkLocationIsSafe(arr, row, col, num):
                arr[row][col] = num
                if self.solveSudoku(arr):
                    return True
                arr[row][col] = 0
        return False
