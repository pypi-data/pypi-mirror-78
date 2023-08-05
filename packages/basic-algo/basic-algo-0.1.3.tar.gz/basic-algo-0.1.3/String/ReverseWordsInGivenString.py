class ReverseWordsInGivenString:
    @staticmethod
    def ReverseWordsInGivenString(s: str) -> str:
        """
        :param s: Input string

        The function reverses the words in a given string

        :return: String with words reversed
        """
        words = s.split(' ')
        string = []
        for word in words:
            string.insert(0, word)
        return " ".join(string)
