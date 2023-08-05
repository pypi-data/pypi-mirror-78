class BinaryTreeFromInorderAndPostorder:
    def __init__(self, data: int):
        """
        :param data: int

        data is the value of node
        """
        try:
            assert isinstance(data, int)
        except AssertionError as _:
            print("vertices should be int.")
            raise
        self.data = data
        self.left = self.right = None

    def buildUtil(self, In: list, post: list, inStart: int, inEnd: int, pIndex: list):
        try:
            assert isinstance(In, list)
        except AssertionError as _:
            print("In should be list.")
            raise
        try:
            assert isinstance(post, list)
        except AssertionError as _:
            print("post should be list.")
            raise
        try:
            assert isinstance(inStart, int)
        except AssertionError as _:
            print("inStart should be int.")
            raise
        try:
            assert isinstance(inEnd, int)
        except AssertionError as _:
            print("inEnd should be int.")
            raise
        try:
            assert isinstance(pIndex, list)
        except AssertionError as _:
            print("pIndex should be int.")
            raise
        if inStart > inEnd:
            return None
        node = BinaryTreeFromInorderAndPostorder(post[pIndex[0]])
        pIndex[0] -= 1
        if inStart == inEnd:
            return node
        iIndex = self.search(In, inStart, inEnd, node.data)
        node.right = self.buildUtil(In, post, iIndex + 1, inEnd, pIndex)
        node.left = self.buildUtil(In, post, inStart, iIndex - 1, pIndex)
        return node

    def buildTree(self, In: list, post: list, n: int) -> None:
        """
        :param In: inorder list
        :param post: postorder list
        :param n: value

        :return: None (Void)
        """
        try:
            assert isinstance(In, list)
        except AssertionError as _:
            print("In should be list.")
            raise
        try:
            assert isinstance(post, list)
        except AssertionError as _:
            print("post should be list.")
            raise
        try:
            assert isinstance(n, int)
        except AssertionError as _:
            print("n should be int.")
            raise
        pIndex = [n - 1]
        return self.buildUtil(In, post, 0, n - 1, pIndex)

    @staticmethod
    def search(arr: list, start: int, end: int, value: int) -> int:
        """
        :param arr: inorder list
        :param start: starting of inorder list
        :param end: ending of inorder list
        :param value: value that to be searched in inorder list

        :return:
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
        i = 0
        for i in range(start, end + 1):
            if arr[i] == value:
                break
        return i
