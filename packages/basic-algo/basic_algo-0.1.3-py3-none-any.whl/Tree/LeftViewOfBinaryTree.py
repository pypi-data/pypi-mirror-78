def leftViewUtil(root, level, max_level):
    if root is None:
        return
    if max_level[0] < level:
        print("% d\t" % root.data, end=' ')
        max_level[0] = level
    leftViewUtil(root.left, level + 1, max_level)
    leftViewUtil(root.right, level + 1, max_level)


class LeftViewOfBinaryTree:
    @staticmethod
    def LeftViewOfBinaryTree(root):
        """
        :param root: root of the binary tree

        Prints left view of the given binary tree

        :return: prints the left view of binary tree
        """
        max_level = [0]
        leftViewUtil(root, 1, max_level)
