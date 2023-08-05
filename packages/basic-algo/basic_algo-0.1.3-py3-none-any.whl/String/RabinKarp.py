class RabinKarp:
    @staticmethod
    def search(pat: str, txt: str, q: int = 101) -> None:
        """
        :param pat: pattern to be searched
        :param txt: the input string in which pattern is to be searched
        :param q: A prime number

        Like the Naive Algorithm, Rabin-Karp algorithm also slides the pattern one by one.
        But unlike the Naive algorithm, Rabin Karp algorithm matches the hash value of the pattern
        with the hash value of current substring of text,
        and if the hash values match then only it starts matching individual characters.
        So Rabin Karp algorithm needs to calculate hash values for following strings.
        1) Pattern itself.
        2) All the substrings of text of length m.

        :return: None (Void)
        """
        d = 256
        M = len(pat)
        N = len(txt)
        j = 0
        p = 0
        t = 0
        h = 1
        for i in range(M - 1):
            h = (h * d) % q
        for i in range(M):
            p = (d * p + ord(pat[i])) % q
            t = (d * t + ord(txt[i])) % q
        for i in range(N - M + 1):
            if p == t:
                for j in range(M):
                    if txt[i + j] != pat[j]:
                        break
                j += 1
                if j == M:
                    print("Pattern found at index " + str(i))
            if i < N - M:
                t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
                if t < 0:
                    t = t + q
