# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 00:23:04 2016

@author: Андрей
"""
#import model
from yat.model import *
class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)
    def visitUnaryOperation(self, expr):
        tmp = expr.expr.visit(self)
        if isinstance(tmp, Number):
            return UnaryOperation(expr.op, tmp).evaluate(None)
    def visitBinaryOperation(self, expr):
        tmpl = expr.lhs.visit(self)
        tmpr = expr.rhs.visit(self)
        if isinstance(tmpl, Number) and isinstance(tmpr, Number):
            return BinaryOperation(tmpl, expr.op, tmpr).evaluate(None)
        elif isinstance(tmpl, Number) and isinstance(tmpr, Reference):
            if not tmpl.value:
                return Number(0)
        elif isinstance(tmpl, Reference) and isinstance(tmpr, Number):
            if not tmpr.value:
                return Number(0)
        elif isinstance(tmpl, Reference) and isinstance(tmpr, Reference) and expr.op == "-":
            if tmpl.name == tmpr.name:
                return Number(0)
            return BinaryOperation(tmpl, expr.op, tmpr)
            
    def visitNumber(self, extra):
        return extra
        
    def visitPrint(self, extra):
        return Print(extra.expr.visit(self))
        
    def visitRead(self, extra):
        return extra
        
    def visitReference(self, extra):
        return extra
        
    def visitFunctionDefinition(self, extra):
        return FunctionDefinition(extra.name, Function(extra.function.args, list(map(lambda x: x.visit(self), extra.function.body))))
    
    def visitFunctionCall(self, extra):
        return FunctionCall(extra.fun_expr.visit(self), list(map(lambda x: x.visit(self), extra.args)))
        
    def visitConditional(self, extra):
        return Conditional(extra.condition.visit(self), list(map(lambda x: x.visit(self), extra.if_true)), list(map(lambda x: x.visit(self), extra.if_false)))
    
    # -*- coding: utf-8 -*-
if __name__ == '__main__':
    pass
    """a = Scope()
    a["cond4"] = BinaryOperation(Number(5), '+', Number(8))
    c = ConstantFolder()
    a['cond4'] = c.visit(a['cond4'])"""