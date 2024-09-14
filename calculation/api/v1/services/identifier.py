import re


async def find_value(data, field):
    for entry in data:
        if field in entry:
            return entry[field]
    return None

# Function to evaluate the sumResult based on the input data


async def evaluate_expression(expression, data):
    stack = []

    for token, token_type in expression:
        if token_type == 'operand':
            if token.isnumeric():
                # If the operand is a number, push it as integer
                stack.append(int(token))
            else:
                # Otherwise, find the value from the input data
                value = await find_value(data, token)
                if value is not None:
                    stack.append(value)
                else:
                    raise ValueError(f"Value for {token} not found in data.")
        elif token_type == 'operator':
            # Apply the operator
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                else:
                    raise ValueError(f"Unsupported operator {token}")
    print(stack)
    return stack[0] if stack else None


async def split_and_identify(expression, data):
    # print(expression)
    exp = {}
    tokens = []
    for formulas in expression:
        # print(formulas)
        # Regular expression pattern to split based on arithmetic operators and parentheses
        pattern = r'([\+\-\*/\(\)])'

        # Split the expression
        for token in re.split(pattern, formulas.get("expression")):
            # print(token, formulas.get('outputVar'))
            stripped_token = token.strip()
            if stripped_token:
                exp.update({formulas.get('outputVar'): []})
                tokens.append({stripped_token: formulas.get('outputVar')})
                exp.update({formulas.get('outputVar'): []})
    # print(tokens)
    # for d in tokens:
    #     s = list(d.keys())
    #     print(s[0])
    # Identify whether each token is an operator or operand
        result = []
        res = {}
        operators = {'+', '-', '*', '/', '(', ')'}
    print(tokens)
    for values in tokens:
        token = list(values.keys())
        print(token[0])
        if token[0] in operators:
            result.append((token[0], 'operator'))
            res.update({token[0]: 'operator'})
        elif token[0] not in {'(', ')'}:  # Ignore parentheses
            result.append((token[0], 'operand'))
            res.update({token[0]: 'operand'})
    print(res)
    # exp.update({formulas.get("outputVar"): result})

    # print(formulas.get("outputVar"))
    # print(exp)
    # for d in exp:
    #     print(d)
    # res = await evaluate_expression(exp.get('sumResult'), data)
    # print(res)

    return expression
