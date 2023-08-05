class EggDropping:
    @staticmethod
    def BinomialCoefficient(x: float, n: int, k: int) -> int:
        """
        :param x: Checking for xth floor
        :param n: Total number of eggs
        :param k: Total number of floors

        Find sum of binomial coefficients
        xCi (where i varies from 1 to n).
        If the sum becomes more than k, return sum

        :return: Sum of binomial coefficients
        """
        try:
            assert isinstance(x, (int, float))
        except AssertionError as _:
            print("x should be float or int.")
            raise
        try:
            assert isinstance(n, int)
        except AssertionError as _:
            print("n should be int.")
            raise
        try:
            assert isinstance(k, int)
        except AssertionError as _:
            print("k should be int.")
            raise
        binomial_sum = 0
        term = 1
        i = 1
        while i <= n and binomial_sum < k:
            term *= x - i + 1
            term /= i
            binomial_sum += term
            i += 1
        return binomial_sum

    def EggDropping(self, n: int, k: int) -> int:
        """
        :param n: Number of eggs
        :param k: Number of floors

        When we drop an egg, two cases arise.
            1. If egg breaks, then we are left with x-1 trials and n-1 eggs.
            2. If egg does not break, then we are left with x-1 trials and n eggs

        :return: Number of minimum trials needed to find the floor below which all floors are safe.
        """
        try:
            assert isinstance(n, int)
        except AssertionError as _:
            print("n should be int.")
            raise
        try:
            assert isinstance(k, int)
        except AssertionError as _:
            print("k should be int.")
            raise
        low = 1
        high = k
        while low < high:
            mid = (low + high) / 2
            if self.BinomialCoefficient(mid, n, k) < k:
                low = mid + 1
            else:
                high = mid
        return int(low)
