# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 00:23:15 2016

@author: Андрей
"""
import printer
import folder
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
    def visit(self, visitor):
        return visitor.visitNumber(self)   
        
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
    def visit(self, visitor):
        return visitor.visitFunctionDefinition(self)
        
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
    def visit(self, visitor):
        return visitor.visitConditional(self)


class Print:

    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, scope):
        result = self.expr.evaluate(scope)
        print(result.value)
        return result
    def visit(self, visitor):
        return visitor.visitPrint(self)

class Read:

    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        num = int(input())
        scope[self.name] = Number(num)
        return scope[self.name]
    def visit(self, visitor):
        return visitor.visitRead(self)

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
    def visit(self, visitor):
        return visitor.visitFunctionCall(self)
class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]
    def visit(self, visitor):
        return visitor.visitReference(self)


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    dct = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
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
    def visit(self, visitor):
        return visitor.visitBinaryOperation(self) 

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
    def visit(self, visitor):
        return visitor.visitUnaryOperation(self)
if __name__ == '__main__':
    pass
    pr1 = printer.PrettyPrinter()
    a = Scope()
    a["ee"] = BinaryOperation(Number(5), "+", BinaryOperation(Number(6), "*", Number(7)))
    pr1.visit(a['ee'])
    a["foo"] = Function(('a1', 'a2',),
                             [Print(Reference('a1')), Print(Reference('a2'))])
    a['ttt'] = FunctionDefinition('foo', a['foo'])
    #pr1.visit(a['ttt'])
    a['rrr'] = FunctionCall(Reference('foo'),
                 [Number(5), Number(3)])
    a["cond3"] = Conditional(Reference('a1'), [Print(Number(5))], [Print(Number(7))])
    a["bazooka"] = Function(('a1', 'a2',),
                             [Print(Reference('a1')), Print(Reference('a2')),
                              Print(BinaryOperation(Reference('a1'), '+', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '-', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '*', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '/', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '<', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '>', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '>=', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '%', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '&&', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '!=', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '||', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '==', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '>=', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '<=', Reference('a2'))),
                              Print(BinaryOperation(Reference('a1'), '-', (BinaryOperation(Reference('a1'), '-', Reference('a2'))))),
                              Print(UnaryOperation('-', Reference('a1'))),
                              Print(UnaryOperation('!', Reference('a1')))])
    pr1.visit(a['ee'])
    pr1.visit(a['rrr'])    
    pr1.visit(a['cond3'])
    pr1.visit(FunctionDefinition('bazooka', a['bazooka']))
    f1 = folder.ConstantFolder()
    a["cond4"] = BinaryOperation(Number(5), '+', Number(8))
    pr1.visit(a['cond4'])
    a['cond4'] = f1.visit(a['cond4'])
    pr1.visit(a['cond4'])
    