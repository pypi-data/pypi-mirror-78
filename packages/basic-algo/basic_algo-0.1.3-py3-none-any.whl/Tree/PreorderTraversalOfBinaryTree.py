class PreorderTraversalOfBinaryTree:
    def PreorderTraversalOfBinaryTree(self, root):
        """
        :param root: root of the tree

        Prints preorder traversal of the given tree

        :return: prints preorder traversal of the given tree
        """
        if root:
            print(root.val)
            self.PreorderTraversalOfBinaryTree(root.left)
            self.PreorderTraversalOfBinaryTree(root.right)
