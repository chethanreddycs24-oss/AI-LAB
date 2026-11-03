def unify(x, y, substitution=None):
    if substitution is None:
        substitution = {}

    if substitution is None:
        return None
    x = substitute(x, substitution)
    y = substitute(y, substitution)

    if x == y:
        return substitution

    if is_variable(x):
        if occurs(x, y):
            return None
        substitution[x] = y
        return substitution

    # If y is a variable
    if is_variable(y):
        if occurs(y, x):
            return None
        substitution[y] = x
        return substitution

    # If both are compound expressions
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return None

        for a, b in zip(x[1:], y[1:]):
            substitution = unify(a, b, substitution)
            if substitution is None:
                return None

        return substitution

    # Different constants
    return None


def is_variable(x):
    return isinstance(x, str) and x.islower() and len(x) == 1


def substitute(x, substitution):
    while is_variable(x) and x in substitution:
        x = substitution[x]

    if isinstance(x, tuple):
        return (x[0],) + tuple(
            substitute(arg, substitution) for arg in x[1:]
        )

    return x


def occurs(variable, expression):
    expression = expression

    if variable == expression:
        return True

    if isinstance(expression, tuple):
        return any(occurs(variable, arg) for arg in expression[1:])

    return False


# Example
expr1 = ("P", "x", "a")
expr2 = ("q", "x", "a")

result = unify(expr1, expr2)

if result is not None:
    print("Unification successful")
    print("MGU:", result)
else:
    print("Unification failed")
