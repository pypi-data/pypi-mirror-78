class HeightOfBinaryTree:
    def HeightOfBinaryTree(self, node):
        """
        :param node: Root of the given binary tree

        Calculates height of the given binary tree

        :return: height of the given binary tree
        """
        if node is None:
            return 0
        else:
            lDepth = self.HeightOfBinaryTree(node.left)
            rDepth = self.HeightOfBinaryTree(node.right)
            if lDepth > rDepth:
                return lDepth + 1
            else:
                return rDepth + 1
