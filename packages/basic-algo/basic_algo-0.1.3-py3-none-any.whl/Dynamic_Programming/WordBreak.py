class WordBreak:
    def wordBreak(self, dictionary, string, lookup):
        """

        :param dictionary: Dictionary holding space separated words
        :param string: Input String
        :param lookup: Array that stores the solution of the sub problem

        Function to determine if can be segmented into a space-separated sequence of one or more dictionary words

        :return: Returns boolean whether the input string can be segmented
        """
        # n stores length of current substring
        n = len(string)

        # return true if we have reached the end of the String
        if n == 0:
            return True

        # if sub-problem is seen for the first time
        if lookup[n] == -1:

            # mark sub-problem as seen (0 initially assuming String
            # can't be segmented)
            lookup[n] = 0

            for i in range(1, n + 1):
                # consider all prefixes of current String
                prefix = string[:i]

                # if prefix is found in dictionary, then recur for suffix
                if prefix in dictionary and self.wordBreak(dictionary, string[i:], lookup):
                    # return true if the can be segmented
                    lookup[n] = 1
                    return True

        # return solution to current sub-problem
        return lookup[n] == 1
