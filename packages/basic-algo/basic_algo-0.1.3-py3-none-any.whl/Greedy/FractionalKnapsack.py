class ItemValue:
    """
    Item Value DataClass
    """
    def __init__(self, wt: int, val: int, ind: int):
        self.wt = wt
        self.val = val
        self.ind = ind
        self.cost = val // wt

    def __lt__(self, other) -> bool:
        return self.cost < other.cost


class FractionalKnapsack:
    """
    obj = FractionalKnapsack()
    weight = [10, 20, 30]
    values = [50, 120, 60]
    W = 50
    print(obj.FractionalKnapsack(weight, values, W))
    """
    @staticmethod
    def FractionalKnapsack(wt: list, val: list, capacity: int) -> float:
        """
        :param wt: List of weights
        :param val: List of values
        :param capacity: Capacity of knapsack

        Finds the maximum value of the weights that can be added to the knapsack.

        :return: Total Value
        """
        temp = []
        iVal = []
        for i in range(len(wt)):
            iVal.append(ItemValue(wt[i], val[i], i))
        iVal.sort(reverse=True)
        totalValue = 0
        for i in iVal:
            curWt = int(i.wt)
            curVal = int(i.val)
            if capacity - curWt >= 0:
                capacity -= curWt
                totalValue += curVal
            else:
                fraction = capacity / curWt
                totalValue += curVal * fraction
                capacity = int(capacity - (curWt * fraction))
                temp.append(capacity)
                break
        return totalValue
