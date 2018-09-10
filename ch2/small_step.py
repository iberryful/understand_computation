import copy

class Number():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def reducible(self):
        return False

class Add():
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

class Multiply():
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

class Boolean():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def reducible(self):
        return False

class LessThan():
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

class Variable():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

class DoNothing():
    def __repr__(self):
        return "do-nothing"

    def reducible(self):
        return False

    def __eq__(self, other):
        return isinstance(other, DoNothing)

class Assign():
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

class Machine():
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
            print(self.statement, self.environment)
            self.step()
        print(self.statement, self.environment)




if __name__ == '__main__':
    add1 = Add(
        Multiply(Number(1), Number(2)),
        Multiply(Number(3), Number(4))
    )
    vm = Machine(add1)
    vm.run()

    Machine(LessThan(Number(5), Add(Number(2), Number(2)))).run()

    Machine(Add(Variable('x'), Variable('y')),
            {'x': Number(3), 'y': Number(4)}
            ).run()

    stmt = Assign('x', Add(Variable('x'), Number(1)))
    env = {'x': Number(2)}
    Machine(stmt, env).run()
