import re

v = int(input())
variables = {}

for _ in range(v):
    name, expr = input().split("=", 1)
    variables[name.strip()] = expr.strip()

expression = input().strip()
memo = {}
visiting = set()


def tokenize(expr):
    return re.findall(r'\d+|[A-Za-z_]\w*|[()+\-*]', expr)


def evaluate_variable(name):
    if name in memo:
        return memo[name]

    if name in visiting:
        raise RuntimeError("CYCLE")

    if name not in variables:
        raise ValueError("INVALID")

    visiting.add(name)
    value = evaluate_expression(variables[name])
    visiting.remove(name)

    memo[name] = value
    return value


def evaluate_expression(expr):
    tokens = tokenize(expr)
    pos = 0

    def parse_expression():
        nonlocal pos
        value = parse_term()

        while pos < len(tokens) and tokens[pos] in "+-":
            op = tokens[pos]
            pos += 1
            right = parse_term()
            value = value + right if op == "+" else value - right

        return value

    def parse_term():
        nonlocal pos
        value = parse_factor()

        while pos < len(tokens) and tokens[pos] == "*":
            pos += 1
            value *= parse_factor()

        return value

    def parse_factor():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError("INVALID")

        token = tokens[pos]

        if token == "(":
            pos += 1
            value = parse_expression()

            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError("INVALID")

            pos += 1
            return value

        if token.isdigit():
            pos += 1
            return int(token)

        if re.fullmatch(r'[A-Za-z_]\w*', token):
            pos += 1
            return evaluate_variable(token)

        raise ValueError("INVALID")

    value = parse_expression()

    if pos != len(tokens):
        raise ValueError("INVALID")

    return value


try:
    print(evaluate_expression(expression))
except RuntimeError:
    print("CYCLE")
except (ValueError, RecursionError):
    print("INVALID")