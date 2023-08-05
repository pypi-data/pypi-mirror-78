class MaxProductSubarray:
    @staticmethod
    def MaxProductSubarray(array: list) -> int:
        """
        :param array: list of sequence

        The following solution assumes that the given input array always has a positive output. The solution works for
        all cases mentioned above. It doesn't work for arrays like {0, 0, -20, 0}, {0, 0, 0}.. etc. The solution can be
        easily modified to handle this case.
        It is similar to Largest Sum Contiguous Subarray problem. The only thing to note here is, maximum product can
        also be obtained by minimum (negative) product ending with the previous element multiplied by this element. For
        example, in array {12, 2, -3, -5, -6, -2}, when we are at element -2, the maximum product is multiplication of,
        minimum product ending with -6 and -2.

        :return: Maximum product subarray
        """
        n = len(array)
        max_ending_here = 1
        min_ending_here = 1
        max_so_far = 1
        flag = 0
        for i in range(0, n):
            if array[i] > 0:
                max_ending_here = max_ending_here * array[i]
                min_ending_here = min(min_ending_here * array[i], 1)
                flag = 1
            elif array[i] == 0:
                max_ending_here = 1
                min_ending_here = 1
            else:
                temp = max_ending_here
                max_ending_here = max(min_ending_here * array[i], 1)
                min_ending_here = temp * array[i]
            if max_so_far < max_ending_here:
                max_so_far = max_ending_here
        if flag == 0 and max_so_far == 1:
            return 0
        return max_so_far
