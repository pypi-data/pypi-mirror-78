class ZeroOneKnapsack:
    @staticmethod
    def ZeroOneKnapsack(values: list, weights: list, capacity: int) -> int:
        """
        :param values: List of values
        :param weights: List of weights of those values
        :param capacity: Capacity

        In the Dynamic programming we will work considering the same cases as mentioned in the recursive approach. In a
        DP[][] table let’s consider all the possible weights from ‘1’ to ‘W’ as the columns and weights that can be
        kept as the rows.
        The state DP[i][j] will denote maximum value of ‘j-weight’ considering all values from ‘1 to ith’. So if we
        consider ‘wi’ (weight in ‘ith’ row) we can fill it in all columns which have ‘weight values > wi’. Now two
        possibilities can take place:
            1. Fill ‘wi’ in the given column.
            2. Do not fill ‘wi’ in the given column.
        Now we have to take a maximum of these two possibilities, formally if we do not fill ‘ith’ weight in ‘jth’
        column then DP[i][j] state will be same as DP[i-1][j] but if we fill the weight, DP[i][j] will be equal to the
        value of ‘wi’+ value of the column weighing ‘j-wi’ in the previous row. So we take the maximum of these two
        possibilities to fill the current state.

        :return: Maximum total value
        """
        try:
            assert isinstance(values, list)
        except AssertionError as _:
            print("Values should be list.")
            raise
        try:
            assert isinstance(weights, list)
        except AssertionError as _:
            print("Weights should be list.")
            raise
        try:
            assert isinstance(capacity, int)
        except AssertionError as _:
            print("Capacity should be int.")
            raise
        dp = [[0 for _ in range(capacity + 1)] for __ in range(len(values) + 1)]
        for v in range(len(values) + 1):
            for c in range(capacity + 1):
                if v == 0 or c == 0:
                    dp[v][c] = 0
                elif weights[v - 1] <= c:
                    dp[v][c] = max(values[v - 1] + dp[v - 1][c - weights[v - 1]], dp[v - 1][c])
                else:
                    dp[v][c] = dp[v - 1][c]
        return dp[len(values)][capacity]
