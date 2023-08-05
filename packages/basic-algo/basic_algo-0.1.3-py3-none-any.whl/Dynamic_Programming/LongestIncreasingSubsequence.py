class LongestIncreasingSubsequence:
    @staticmethod
    def LongestIncreasingSubsequence(array: list) -> int:
        """
        :param array: list of sequence

        This problem has Overlapping Substructure property and re-computation of same sub-problems can be avoided by
        either using Memoization or Tabulation.

        :return: Longest increasing subsequence
        """
        try:
            assert isinstance(array, list)
        except AssertionError as _:
            print("Array should be list.")
            raise
        n = len(array)
        LIS = [1] * n
        for i in range(1, n):
            for j in range(0, i):
                if array[i] > array[j] and LIS[i] < LIS[j] + 1:
                    LIS[i] = LIS[j] + 1
        maximum = 0
        for i in range(n):
            maximum = max(maximum, LIS[i])
        return maximum
