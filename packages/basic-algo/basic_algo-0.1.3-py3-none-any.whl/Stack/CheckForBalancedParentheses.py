class CheckForBalancedParentheses:
    """
    obj = CheckForBalancedParentheses()
    print(obj.Check_For_Balanced_Parentheses("((()))"))
    """
    @staticmethod
    def Check_For_Balanced_Parentheses(expr: str) -> bool:
        """
        :param expr: Input expression to be checked

        Declare a character stack S. Traverse the expression and push if it is an opening braces
        else pop if its matching closing braces appear else return false

        :return: True or false whether the parenthesis are valid
        """
        stack = []
        for char in expr:
            if char in ["(", "{", "["]:
                stack.append(char)
            else:
                if not stack:
                    return False
                current_char = stack.pop()
                if current_char == '(':
                    if char != ")":
                        return False
                if current_char == '{':
                    if char != "}":
                        return False
                if current_char == '[':
                    if char != "]":
                        return False
        if stack:
            return False
        return True
