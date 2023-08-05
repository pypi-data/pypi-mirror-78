def computeLPSArray(pat: str, M: int, lps: list) -> None:
    """
    :param pat: pattern
    :param M: length of pattern
    :param lps: list of LPS

    Computing LPS array

    :return: None (Void)
    """
    length = 0
    i = 1
    while i < M:
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1


class KMPAlgorithm:
    """
    obj = KMPAlgorithm()
    obj.KMPSearch("aaa", "aaabbbaaabbbaaabbbababaaa")
    """
    @staticmethod
    def KMPSearch(pat: str, txt: str) -> None:
        """
        :param pat: Pattern to be searched
        :param txt: Input string in which the pattern is to be searched

        Unlike Naive algorithm, where we slide the pattern by one and compare all characters at each shift,
        we use a value from lps[] to decide the next characters to be matched.
        The idea is to not match a character that we know will anyway match.

        :return: None (Void)
        """
        M = len(pat)
        N = len(txt)
        lps = [0] * M
        j = 0
        computeLPSArray(pat, M, lps)
        i = 0
        while i < N:
            if pat[j] == txt[i]:
                i += 1
                j += 1
            if j == M:
                print("Found pattern at index " + str(i - j))
                j = lps[j - 1]
            elif i < N and pat[j] != txt[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
