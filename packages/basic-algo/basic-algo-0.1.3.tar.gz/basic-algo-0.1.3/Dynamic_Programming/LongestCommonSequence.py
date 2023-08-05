class ClassName:
    def LongestCommonSubsequence(self, arr, n):

        """
        :param arr : List of integers
        :param n : Length of list of integers

        The idea is to use Hashing. We first insert all elements in a Set.
        Then check all the possible starts of consecutive subsequences.

        :return : length of the longest sub-sequence such that elements in the subsequence are consecutive integers
        """

        s = set()
        ans = 0

        # Hash all the array elements 
        for ele in arr:
            s.add(ele)

            # check each possible sequence from the start
        # then update optimal length 
        for i in range(n):

            # if current element is the starting
            # element of a sequence 
            if (arr[i] - 1) not in s:

                # Then check for next elements in the 
                # sequence 
                j = arr[i]
                while j in s:
                    j += 1

                # update  optimal length if this length 
                # is more 
                ans = max(ans, j - arr[i])
        return ans
