class CoinChange:
    @staticmethod
    def CoinChange(array: list, amount: int) -> int:
        """
        :param array: list of denominations.
        :param amount: Given value of amount.

        To count the total number of solutions, we can divide all set solutions into two sets.
            1) Solutions that do not contain mth coin (or Sm).
            2) Solutions that contain at least one Sm.
        Let count(S[], m, n) be the function to count the number of solutions, then it can be written as sum of
        count(S[], m-1, n) and count(S[], m, n-Sm).
        Since same sub-problems are called again, this problem has Overlapping Sub-problems property. So the Coin Change
        problem has both properties of a dynamic programming problem. Like other typical Dynamic_Programming(DP)
        problems, re-computations of same sub-problems can be avoided by constructing a temporary array
        table[][] in bottom up manner.

        :return: Number of ways we can make change
        """
        try:
            assert isinstance(array, list)
        except AssertionError as _:
            print("Array should be list.")
            raise
        m = len(array)
        table = [0 for _ in range(amount + 1)]
        table[0] = 1
        for i in range(0, m):
            for j in range(array[i], amount + 1):
                table[j] += table[j - array[i]]
        return table[amount]
