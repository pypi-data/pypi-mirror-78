class InorderTraversalOfBinaryTree:
    def InorderTraversalOfBinaryTree(self, root):
        """
        :param root: root of the tree

        Prints inorder traversal of the given tree

        :return: prints inorder traversal of the given tree
        """
        if root:
            self.InorderTraversalOfBinaryTree(root.left)
            print(root.val)
            self.InorderTraversalOfBinaryTree(root.right)
