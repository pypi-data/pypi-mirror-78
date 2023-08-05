import math


class KthPermutationSequence:
    """
    obj = KthPermutationSequence()
    print(obj.Kth_Permutation_Sequence(7, 4))
    """
    @staticmethod
    def Kth_Permutation_Sequence(n: int, k: int) -> str:
        """
        :param n: length of sequence
        :param k: kth permutation

        The first position of an n length sequence is occupied by each of the numbers from 1 to n exactly n! / n that is
        (n-1)! number of times and in ascending order. So the first position of the kth sequence will be occupied by the
        number present at index = k / (n-1)! (according to 1-based indexing).
        The currently found number can not occur again so it is removed from the original n numbers and now the problem
        reduces to finding the ( k % (n-1)! )th permutation sequence of the remaining n-1 numbers.
        This process can be repeated until we have only one number left which will be placed in the first position of
        the last 1-length sequence.
        The factorial values involved here can be very large as compared to k. So, the trick used to avoid the full
        computation of such large factorials is that as soon as the product n * (n-1) * … becomes greater than k, we no
        longer need to find the actual factorial value because:

        :return: String containing the kth permutation of the input sequence
        """
        numbers = list(range(1, n + 1))
        permutation = ''
        k -= 1
        while n > 0:
            n -= 1
            index, k = divmod(k, math.factorial(n))
            permutation += str(numbers[index])
            del numbers[index]
        return permutation
