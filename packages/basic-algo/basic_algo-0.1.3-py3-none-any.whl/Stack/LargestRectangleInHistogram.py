class LargestRectangleInHistogram:
    """
    obj = LargestRectangleInHistogram()
    print(obj.LargestRectangleInHistogram([5, 3, 6, 4, 7, 3, 2]))
    """
    @staticmethod
    def LargestRectangleInHistogram(histogram: list) -> int:
        """
        :param histogram: the input histogram in the form of array

        This function calculates maximum rectangular area under given histogram with n bars
        Create an empty stack. The stack holds indexes of histogram[] list.
        The bars stored in the stack are always in increasing order of their heights.

        :return: returns the area of the largest rectangle in the input histogram
        """
        stack = list()
        max_area = 0
        index = 0
        while index < len(histogram):
            if (not stack) or (histogram[stack[-1]] <= histogram[index]):
                stack.append(index)
                index += 1
            else:
                top_of_stack = stack.pop()
                area = (histogram[top_of_stack] * ((index - stack[-1] - 1) if stack else index))
                max_area = max(max_area, area)
        while stack:
            top_of_stack = stack.pop()
            area = (histogram[top_of_stack] * ((index - stack[-1] - 1) if stack else index))
            max_area = max(max_area, area)
        return max_area
