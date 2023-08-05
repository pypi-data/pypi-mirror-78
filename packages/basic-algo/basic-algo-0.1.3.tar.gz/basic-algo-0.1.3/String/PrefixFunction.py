class PrefixFunction:
    @staticmethod
    def PrefixFunction(s: str) -> int:
        """
        :param s: Input string

        Returns length of the longest prefix which is also suffix and the two do not overlap.

        :return: Length of the longest prefix which is also suffix
        """
        n = len(s)
        lps = [0] * n
        track = 0
        i = 1
        while i < n:
            if s[i] == s[track]:
                track = track + 1
                lps[i] = track
                i = i + 1
            else:
                if track != 0:
                    track = lps[track - 1]
                else:
                    lps[i] = 0
                    i = i + 1
        res = lps[n - 1]
        if res > n / 2:
            return n // 2
        else:
            return res
