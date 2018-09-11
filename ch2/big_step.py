import copy


class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def reducible(self):
        return False

    def evaluate(self, environment=None):
        return self


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{left} + {right}'.format(left=repr(self.left), right=repr(self.right))

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def evaluate(self, environment=None):
        return Number(
            self.left.evaluate(environment).value + \
            self.right.evaluate(environment).value
        )


class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{left} * {right}'.format(left=repr(self.left), right=repr(self.right))

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)

    def evaluate(self, environment=None):
        return Number(
            self.left.evaluate(environment).value * \
            self.right.evaluate(environment).value
        )


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def reducible(self):
        return False

    def evaluate(self, environment=None):
        return self


class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return '{left} < {right}'.format(left=repr(self.left), right=repr(self.right))

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def evaluate(self, environment=None):
        return Boolean(
            self.left.evaluate(environment).value < \
            self.right.evaluate(environment).value
        )


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def evaluate(self, environment):
        return environment[self.name]


class DoNothing:
    def __repr__(self):
        return "do-nothing"

    def reducible(self):
        return False

    def __eq__(self, other):
        return isinstance(other, DoNothing)

    def evaluate(self, environment):
        return environment


class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def reducible(self):
        return True

    def __repr__(self):
        return '{name} = {expression}'.format(name=str(self.name), expression=repr(self.expression))

    def reduce(self, environment=None):
        if self.expression.reducible():
            return (Assign(self.name, self.expression.reduce(environment)), environment)
        else:
            new_environment = copy.deepcopy(environment)
            new_environment.update({self.name: self.expression})
            return (DoNothing(), new_environment)

    def evaluate(self, environment):
        new_value = self.expression.evaluate(environment)
        new_env = copy.deepcopy(environment)
        new_env.update({self.name: new_value})
        return new_env


class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __repr__(self):
        return "if (%s) {%s} else {%s}" % (
            repr(self.condition), repr(self.consequence), repr(self.alternative))

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible():
            return (If(self.condition.reduce(environment), self.consequence, self.alternative), environment)
        else:
            if self.condition.value:
                return (self.consequence, environment)
            else:
                return (self.alternative, environment)

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.consequence.evaluate(environment)
        else:
            return self.alternative.evaluate(environment)


class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return "%s; %s" % (repr(self.first), repr(self.second))

    def reducible(self):
        return True

    def reduce(self, environment):
        if isinstance(self.first, DoNothing):
            return (self.second, environment)
        else:
            reduced_first, reduced_environment = self.first.reduce(environment)
            return (Sequence(reduced_first, self.second), reduced_environment)

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return "while (%s) {%s}" % (repr(self.condition), repr(self.body))

    def reducible(self):
        return True

    def reduce(self, environment):
        return (If(self.condition, Sequence(self.body, While(self.condition, self.body)), DoNothing()), environment)

    def evaluate(self, environment):
        if self.condition.evaluate(environment) == Boolean(True):
            return self.evaluate(self.body.evaluate(environment))
        else:
            return environment

class Machine:
    def __init__(self, statement, environment=None):
        self.statement = statement
        self.environment = environment

    def step(self):
        result = self.statement.reduce(self.environment)
        if isinstance(result, tuple):
            self.statement, self.environment = result
        else:
            self.statement = result

    def run(self):
        while self.statement.reducible():
            print(self.statement, self.environment, sep=',')
            self.step()
        print(self.statement, self.environment, sep=',')


if __name__ == '__main__':
    print(Number(23).evaluate({}))
    print(
        LessThan(
            Add(Variable('x'), Number(2)),
            Variable('y')
        ).evaluate({'x': Number(2), 'y': Number(5)})
    )

    print(
        Sequence(
            Assign('x', Add(Number(1), Number(1))),
            Assign('y', Add(Variable('x'), Number(3)))
        ).evaluate({})
    )

    print(
        While(
            LessThan(Variable('x'), Number(5)),
            Assign('x', Multiply(Variable('x'), Number(3)))
        ).evaluate({'x': Number(1)})
    )
