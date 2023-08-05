class SubsetSum:
    @staticmethod
    def SubsetSum(array: list, target: int) -> bool:
        """
        :param array: list of numbers from which target is to be achieved
        :param target: Target sum to be achieved

        For the recursive approach we will consider two cases.
            1. Consider the last element and now the required sum = target sum – value of ‘last’ element and number of
               elements = total elements – 1
            2. Leave the ‘last’ element and now the required sum = target sum and number of elements = total elements –
               1
        To solve the problem in Pseudo-polynomial time use the Dynamic programming.
        So we will create a 2D array of size (arr.size() + 1) * (target + 1) of type boolean.The state DP[i][j] will be
        true if there exists a subset of elements from A[0….i] with sum value = ‘j’.
        The solution discussed above requires O(n * sum) space and O(n * sum) time. We can optimize space. We create a
        boolean 2D array subset[2][sum+1]. Using bottom up manner we can fill up this table. The idea behind using 2 in
        “subset[2][sum+1]” is that for filling a row only the values from previous row is required. So alternate rows
        are used either making the first one as current and second as previous or the first as previous and second as
        current.

        :return: Whether or not the target is achieved
        """
        try:
            assert isinstance(array, list)
        except AssertionError as _:
            print("Array should be list.")
            raise
        try:
            assert isinstance(target, int)
        except AssertionError as _:
            print("Target should be int.")
            raise
        n = len(array)
        if n == 0:
            return False
        subset = [[False for _ in range(target + 1)] for __ in range(3)]
        for i in range(n + 1):
            for j in range(target + 1):
                if j == 0:
                    subset[i % 2][j] = True
                elif i == 0:
                    subset[i % 2][j] = False
                elif array[i - 1] <= j:
                    subset[i % 2][j] = subset[(i + 1) % 2][j - array[i - 1]] or subset[(i + 1) % 2][j]
                else:
                    subset[i % 2][j] = subset[(i + 1) % 2][j]
        return subset[n % 2][target]
