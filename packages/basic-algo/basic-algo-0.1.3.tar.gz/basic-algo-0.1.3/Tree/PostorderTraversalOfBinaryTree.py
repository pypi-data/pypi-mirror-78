class PostorderTraversalOfBinaryTree:
    def PostorderTraversalOfBinaryTree(self, root):
        """
        :param root: root of the tree

        Prints postorder traversal of the given tree

        :return: prints postorder traversal of the given tree
        """
        if root:
            self.PostorderTraversalOfBinaryTree(root.left)
            self.PostorderTraversalOfBinaryTree(root.right)
            print(root.val)
