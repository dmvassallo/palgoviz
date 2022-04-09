#!/usr/bin/env python

"""Calculator."""


def postfix_calculate(expression):
    """
    Simplify a well-formed postfix arithmetic expression, returning a float.

    The expression consists of tokens separated by whitespace, where each token
    either can be interpreted as a floating-point number or is one of the
    symbols "+", "-", "*", or "/", denoting a binary arithmetic operation.

    In postfix notation, operands precede the operator that operates on them.

    >>> postfix_calculate('3')
    3.0
    >>> postfix_calculate('3 4 +')
    7.0
    >>> postfix_calculate('1 3 + 2 7 - /')
    -0.8
    >>> postfix_calculate('1 3 2 / + 7 -')
    -4.5
    >>> round(postfix_calculate('3 2.2 * 1 + 1 2 / -'), 10)
    7.1
    """
    # step 1, Build the list I want
    tokens = expression.split()

    while len(tokens) > 1:
        #find first operator w/o modifying the list
        for index, element in enumerate(tokens):
            if element == '+':
                result = float(tokens[index - 2]) + float(tokens[index - 1])
            elif element == '-':
                result = float(tokens[index - 2]) - float(tokens[index - 1])
            elif element == '*':
                result = float(tokens[index - 2]) * float(tokens[index - 1])
            elif element == '/':
                result = float(tokens[index - 2]) / float(tokens[index - 1])
            else:
                continue

            tokens.pop(index)
            tokens.pop(index - 1)
            tokens.pop(index - 2)
            tokens.insert(index - 2, result)
            break

    return float(tokens.pop())
