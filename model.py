class Scope(object):
    
    def __init__(self, parent = None):
        self.parent = parent
        self.dictionary = dict()
        
    def __setitem__(self, key, value):
        self.dictionary[key] = value
        
    def __getitem__(self, key):
        if key not in self.dictionary:
            if self.parent:
                return self.parent[key]
        return self.dictionary[key]
    
class Number:
    def __init__(self, value):
        self.value = value
        
    def evaluate(self, scope):
        return self  
        
class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body
        
    def evaluate(self, scope):
        function_value = None
        for action in self.body:
            function_value = action.evaluate(scope)
        return function_value
        
class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function
        
class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        condition_result = None
        branch = self.if_true if self.condition.evaluate(scope).value else self.if_false
        if branch is not None:
            for i in branch:
                condition_result = i.evaluate(scope)
        return condition_result

class Print:

    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, scope):
        result = self.expr.evaluate(scope)
        print(result.value)
        return result

class Read:

    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        num = int(input())
        scope[self.name] = Number(num)
        return scope[self.name]


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        self.function = self.fun_expr.evaluate(scope)
        self.call_scope = Scope(scope)
        for name, ar in zip(self.function.args, self.args):
            self.call_scope[name] = ar.evaluate(scope)
        return self.function.evaluate(self.call_scope)

class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    dct = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x // y,
    '%': lambda x, y: x % y,
    '&&': lambda x, y: 1 if x and y else 0,
    '||': lambda x, y: 1 if x or y else 0,
    '==': lambda x, y: 1 if x == y else 0,
    '!=': lambda x, y: 1 if x != y else 0,
    '<': lambda x, y: 1 if x < y else 0,
    '>': lambda x, y: 1 if x > y else 0,
    '<=': lambda x, y: 1 if x <= y else 0,
    '>=': lambda x, y: 1 if x >= y else 0,
    }

    def evaluate(self, scope):
        return Number(self.dct[self.op](self.lhs.evaluate(scope).value, self.rhs.evaluate(scope).value))

class UnaryOperation:
    dct = {
    '-': lambda x: -x,
    '!': lambda x: not x  
    }
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(self.dct[self.op](self.expr.evaluate(scope).value))
