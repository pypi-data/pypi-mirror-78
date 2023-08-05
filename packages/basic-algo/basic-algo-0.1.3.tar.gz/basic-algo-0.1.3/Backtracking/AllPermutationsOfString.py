class AllPermutationsOfString:
    """
    obj = AllPermutationsOfString()
    string = "123"
    obj.permute(list(string), 0, len(string))
    print(obj.result)
    """
    def __init__(self):
        self.result = []

    def permute(self, data: list, left: int, right: int) -> None:
        """
        :param data: String
        :param left: Starting index of the string
        :param right: Ending index of the string

        Function to print permutations of string

        :return: None (Void)
        """
        if left == right:
            self.result.append(''.join(data))
        else:
            for j in range(left, right):
                data[left], data[j] = data[j], data[left]
                self.permute(data, left + 1, right)
                data[left], data[j] = data[j], data[left]
