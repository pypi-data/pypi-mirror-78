from sys import maxsize


class Node:
    def __init__(self, data: int) -> None:
        """
        :param data : value

        Intialising node
        """
        try:
            assert isinstance(data, int)
        except AssertionError as _:
            print("data should be int.")
            raise
        self.data = data
        self.left = None
        self.right = None


class BinaryTreeFromInorderAndPreorder:
    def buildTree(self, inOrder: list, preOrder: list, inStart: int, inEnd: int) -> Node:
        """
        :param inOrder : list of node in inOrder traversal
        :param preOrder : list of node in preOrder traversal
        :param inStart : starting of inorder list
        :param inEnd : Ending of inorder list

        building binary tree
        """
        try:
            assert isinstance(inOrder, list)
        except AssertionError as _:
            print("Inorder should be list.")
            raise
        try:
            assert isinstance(preOrder, list)
        except AssertionError as _:
            print("preorder should be int.")
            raise
        try:
            assert isinstance(inStart, int)
        except AssertionError as _:
            print("inStrt should be int.")
            raise
        try:
            assert isinstance(inEnd, int)
        except AssertionError as _:
            print("inEnd should be int.")
            raise
        if inStart > inEnd:
            temp = Node(-1)
            return temp
        tNode = Node(preOrder[self.buildTree.preIndex])
        self.buildTree.preIndex += 1

        if inStart == inEnd:
            return tNode

        inIndex = self.search(inOrder, inStart, inEnd, tNode.data)

        tNode.left = self.buildTree(inOrder, preOrder, inStart, inIndex - 1)
        tNode.right = self.buildTree(inOrder, preOrder, inIndex + 1, inEnd)
        return tNode

    @staticmethod
    def search(arr: list, start: int, end: int, value: int) -> int:
        """
        :param arr : list of node in inoder traversal
        :param start : starting of inorder list
        :param end : Endining of inorder list
        :param value : the value to be searched in inorder

        building binary tree
        """
        try:
            assert isinstance(arr, list)
        except AssertionError as _:
            print("arr should be list.")
            raise
        try:
            assert isinstance(start, int)
        except AssertionError as _:
            print("start should be int.")
            raise
        try:
            assert isinstance(end, int)
        except AssertionError as _:
            print("end should be int.")
            raise
        try:
            assert isinstance(value, int)
        except AssertionError as _:
            print("value should be int.")
            raise
        for i in range(start, end + 1):
            if arr[i] == value:
                return i
