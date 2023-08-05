def findMinLength(arr):
    return len(min(arr, key=len))


def allContainsPrefix(strList: list, string: str, start: int, end: int) -> bool:
    for i in range(0, len(strList)):
        word = strList[i]
        for j in range(start, end + 1):
            if word[j] != string[j]:
                return False
    return True


class LongestCommonPrefix:
    @staticmethod
    def CommonPrefix(strList: list) -> str:
        """
        :param strList: list of strings

        Given a set of strings, find the longest common prefix.

        :return: string containing longest common prefix
        """
        index = findMinLength(strList)
        prefix = ""
        low, high = 0, index - 1
        while low <= high:
            mid = int(low + (high - low) / 2)
            if allContainsPrefix(strList, strList[0], low, mid):
                prefix = prefix + strList[0][low:mid + 1]
                low = mid + 1
            else:
                high = mid - 1
        return prefix
