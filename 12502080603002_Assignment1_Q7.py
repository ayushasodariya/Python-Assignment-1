import re

class InvalidFormatError(Exception):
    pass

class UnknownVariableError(Exception):
    pass

class DivisionByZeroError(Exception):
    pass

class UnsupportedOperatorError(Exception):
    pass

def get_value(value, variables):
    """Get a number directly or fetch it from stored variables."""

    # Check if the value is an integer or decimal.
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    # If it is not a number, check the variable dictionary.
    if value in variables:
        return variables[value]

    raise UnknownVariableError(f"Unknown variable: {value}")


def calculate(left, operator, right):
    """Perform the requested calculation."""

    if operator not in ["+", "-", "*", "/", "%"]:
        raise UnsupportedOperatorError(
            f"Unsupported operator: {operator}"
        )

    if operator == "/" and right == 0:
        raise DivisionByZeroError("Cannot divide by zero")

    if operator == "%" and right == 0:
        raise DivisionByZeroError("Cannot divide by zero")

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":
        return left / right

    return left % right


def process_line(line, variables):
    """Process either a variable assignment or a formula."""

    # Handle assignments such as: x = 10
    if "=" in line:
        parts = line.split("=")

        if len(parts) != 2:
            raise InvalidFormatError("Invalid assignment")

        variable = parts[0].strip()
        value_text = parts[1].strip()

        if not variable.isidentifier():
            raise InvalidFormatError("Invalid variable name")

        if not value_text:
            raise InvalidFormatError("Missing value")

        value = get_value(value_text, variables)
        variables[variable] = value

        return None

    # Formula should have exactly: operand operator operand
    parts = line.split()

    if len(parts) != 3:
        raise InvalidFormatError(
            "Formula must be: operand operator operand"
        )

    left_text, operator, right_text = parts

    # A special operator such as ** should be reported separately.
    if operator not in ["+", "-", "*", "/", "%"]:
        raise UnsupportedOperatorError(
            f"Unsupported operator: {operator}"
        )

    left = get_value(left_text, variables)
    right = get_value(right_text, variables)

    return calculate(left, operator, right)


def main():
    variables = {}

    print("Enter formula (type quit to stop):")

    while True:
        try:
            line = input("> ").strip()

            if line.lower() == "quit":
                break

            if not line:
                raise InvalidFormatError("Empty input")

            result = process_line(line, variables)

            # Assignments don't have a result to print.
            if result is not None:
                print(result)

        except (
            InvalidFormatError,
            UnknownVariableError,
            DivisionByZeroError,
            UnsupportedOperatorError
        ) as error:
            print(type(error).__name__)
            print(error)


if __name__ == "__main__":
    main()