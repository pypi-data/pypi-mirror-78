from sys import maxsize


class PalindromePartitioning:
    @staticmethod
    def PalindromePartitioning(string: str) -> int:
        """
        :param string: Input string to find partitions.

        If the string is a palindrome, then we simply return 0. Else, like the Matrix Chain Multiplication problem,
        we try making cuts at all possible places, recursively calculate the cost for each cut and return the minimum
        value. Using Dynamic_Programming, we store the solutions to sub-problems in two arrays P[][] and C[][], and
        reuses the calculated values. We can optimize this method a bit further. Instead of calculating C[i]
        separately in O(n^2), we can do it with the P[i] itself. In this approach, we can calculate the minimum cut
        while finding all palindromic substring. If we find all palindromic substring 1st and then we calculate minimum
        cut, time complexity will reduce to O(n^2).

        :return: Minimum cuts needed for palindrome partitioning.
        """
        try:
            assert isinstance(string, str)
        except AssertionError as _:
            print("string should be of type str.")
            raise
        N = len(string)
        if N == 0:
            return 0
        C = [0] * (N + 1)
        P = [[False for _ in range(N + 1)] for __ in range(N + 1)]
        for i in range(N):
            P[i][i] = True
        for L in range(2, N + 1): 
            for i in range(N - L + 1):
                j = i + L - 1
                if L == 2:
                    P[i][j] = (string[i] == string[j])
                else:
                    P[i][j] = ((string[i] == string[j]) and P[i + 1][j - 1])
        for i in range(N):
            if P[0][i]:
                C[i] = 0
            else:
                C[i] = maxsize
                for j in range(i):
                    if P[j + 1][i] and 1 + C[j] < C[i]:
                        C[i] = 1 + C[j] 
        return C[N - 1]
