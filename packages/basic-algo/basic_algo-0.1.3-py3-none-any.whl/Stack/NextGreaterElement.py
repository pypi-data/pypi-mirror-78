def createStack():
    stack = []
    return stack


def isEmpty(stack):
    return len(stack) == 0


def push(stack, x):
    stack.append(x)


def pop(stack):
    if isEmpty(stack):
        print("Error : stack underflow")
    else:
        return stack.pop()


class NextGreaterElement:
    """
    obj = NextGreaterElement()
    obj.printNGE([4, 2, 5, 3, 6, 1, 7])
    """
    @staticmethod
    def printNGE(arr: list) -> None:
        """
        :param arr: The input array

        Given an array, print the Next Greater Element (NGE) for every element.
        The Next greater Element for an element x is the first greater element on the right side of x in array.
        Elements for which no greater element exist, consider nxt greater element as -1.

        :return: None (Void)
        """
        s = createStack()
        push(s, arr[0])
        for i in range(1, len(arr), 1):
            nxt = arr[i]
            if not isEmpty(s):
                element = pop(s)
                while element < nxt:
                    print(str(element) + " -- " + str(nxt))
                    if isEmpty(s):
                        break
                    element = pop(s)
                if element > nxt:
                    push(s, element)
            push(s, nxt)
        while not isEmpty(s):
            element = pop(s)
            nxt = -1
            print(str(element) + " -- " + str(nxt))
