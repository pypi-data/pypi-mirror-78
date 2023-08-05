from sys import maxsize

class KadanesAlgorithm:
    def KadanesAlgorithm(self, arr):
        """
        :param arr: List of integers

        Simple idea of the Kadane’s algorithm is to look for all positive contiguous segments of the array
        (max_ending_here is used for this). And keep track of maximum sum contiguous segment among all positive segments
        (max_so_far is used for this). Each time we get a positive sum compare it with max_so_far and update max_so_far
        if it is greater than max_so_far. Program can be optimized further, if we compare max_so_far with
        max_ending_here only if max_ending_here is greater than 0.
        
        :return: Maximum sum subarray
        """
        max_so_far = -maxsize - 1
        max_ending_here = 0
        for i in range(0, len(arr)):
            max_ending_here = max_ending_here + arr[i]
            if (max_so_far < max_ending_here):
                max_so_far = max_ending_here
            if max_ending_here < 0:
                max_ending_here = 0
        return max_so_far
