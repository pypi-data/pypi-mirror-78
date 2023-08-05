def findMaxUtil(root):
    if root is None:
        return 0
    l = findMaxUtil(root.left)
    r = findMaxUtil(root.right)
    max_single = max(max(l, r) + root.data, root.data)
    max_top = max(max_single, l + r + root.data)
    findMaxUtil.res = max(findMaxUtil.res, max_top)
    return max_single


class MaximumPathSumInBinaryTree:
    @staticmethod
    def findMaxSum(root):
        """
        :param root: root of the given binary tree

        Prints maximum path sum in the given binary tree

        :return: returns maximum path sum of the given binary tree
        """
        findMaxUtil.res = float("-inf")
        findMaxUtil(root)
        return findMaxUtil.res
