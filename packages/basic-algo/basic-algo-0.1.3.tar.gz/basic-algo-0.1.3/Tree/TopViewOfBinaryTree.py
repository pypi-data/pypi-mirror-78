def fillMap(root, d, track, m):
    if root is None:
        return
    if d not in m:
        m[d] = [root.data, track]
    elif m[d][1] > track:
        m[d] = [root.data, track]
    fillMap(root.left, d - 1, track + 1, m)
    fillMap(root.right, d + 1, track + 1, m)


class TopViewOfBinaryTree:
    @staticmethod
    def TopViewOfBinaryTree(root):
        """
        :param root: root of the given binary tree

        Prints the top view of the given binary tree

        :return: prints the top view of the given binary tree
        """
        m = {}
        fillMap(root, 0, 0, m)
        for it in sorted(m.keys()):
            print(m[it][0], end=" ")
