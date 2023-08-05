def printBottom(root, dist, level, dictionary):
    if root is None:
        return
    if dist not in dictionary or level >= dictionary[dist][1]:
        dictionary[dist] = (root.data, level)
    printBottom(root.left, dist - 1, level + 1, dictionary)
    printBottom(root.right, dist + 1, level + 1, dictionary)


class BottomViewOfBinaryTree:
    @staticmethod
    def BottomViewOfBinaryTree(root):
        """
        :param root: root of the given binary tree

        Prints the bottom view of the given binary tree

        :return: prints the bottom view of the given binary tree
        """
        dictionary = {}
        printBottom(root, 0, 0, dictionary)
        for key in sorted(dictionary.keys()):
            print(dictionary.get(key)[0], end=' ')
