import math
import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log10,
    "ln": math.log,
    "factorial": math.factorial,
    "abs": abs,
}


def safe_calculate(expression):

    if not isinstance(expression, str):
        raise ValueError("Invalid expression")

    if len(expression) > 300:
        raise ValueError("Expression too long")

    expression = expression.replace("^", "**")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)

        if isinstance(result, float):
            if not math.isfinite(result):
                raise ValueError("Invalid result")

        return result

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")

    except Exception as error:
        raise ValueError(str(error))


def evaluate(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid number")

    elif isinstance(node, ast.BinOp):

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        left = evaluate(node.left)
        right = evaluate(node.right)

        if operator_type == ast.Pow and abs(right) > 1000:
            raise ValueError("Power limit exceeded")

        return OPERATORS[operator_type](left, right)

    elif isinstance(node, ast.UnaryOp):

        operator_type = type(node.op)

        if operator_type not in OPERATORS:
            raise ValueError("Invalid operator")

        return OPERATORS[operator_type](
            evaluate(node.operand)
        )

    elif isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        name = node.func.id

        if name not in FUNCTIONS:
            raise ValueError("Unknown function")

        if len(node.args) != 1:
            raise ValueError("Invalid arguments")

        value = evaluate(node.args[0])

        if name == "factorial":
            if not isinstance(value, int) or value < 0 or value > 1000:
                raise ValueError("Invalid factorial")

        return FUNCTIONS[name](value)

    elif isinstance(node, ast.Name):

        constants = {
            "pi": math.pi,
            "e": math.e
        }

        if node.id in constants:
            return constants[node.id]

        raise ValueError("Unknown constant")

    else:
        raise ValueError("Invalid expression")