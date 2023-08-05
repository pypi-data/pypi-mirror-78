def rightViewUtil(root, level, max_level):
    if root is None:
        return
    if max_level[0] < level:
        print("%d   " % root.data, end=' ')
        max_level[0] = level
    rightViewUtil(root.right, level + 1, max_level)
    rightViewUtil(root.left, level + 1, max_level)


class RightViewOfBinaryTree:
    @staticmethod
    def RightViewOfBinaryTree(root):
        """
        :param root: root of the given binary tree

        Prints the right view of the given binary tree

        :return: prints right view of the given binary tree
        """
        max_level = [0]
        rightViewUtil(root, 1, max_level)
