class LongestCommonSubsequence:
    def LongestCommonSubsequence(self, string_1: str, string_2: str) -> int:
        """
        :param string_1: string 1
        :param string_2: string 2

        This problem has Overlapping Substructure property and re-computation of same sub-problems can be avoided by
        either using Memoization or Tabulation.

        :return: Longest Common Subsequence
        """
        try:
            assert isinstance(string_1, str)
        except AssertionError as _:
            print("String 1 should be str.")
            raise
        try:
            assert isinstance(string_2, str)
        except AssertionError as _:
            print("String 2 should be str.")
            raise
        n = len(string_1)
        m = len(string_2)
        L = [[-1 for _ in range(m + 1)] for __ in range(n + 1)]
        for i in range(n + 1):
            for j in range(m + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif string_1[i - 1] == string_2[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])
        return L[n][m]
