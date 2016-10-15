# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 00:23:04 2016

@author: Андрей
"""
import model
class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)
    def visitUnaryOperation(self, expr):
        tmp = expr.expr.visit(self)
        if isinstance(tmp, model.Number):
            return model.UnaryOperation(expr.op, tmp).evaluate(None)
    def visitBinaryOperation(self, expr):
        tmpl = expr.lhs.visit(self)
        tmpr = expr.rhs.visit(self)
        if isinstance(tmpl, model.Number) and isinstance(tmpr, model.Number):
            return model.BinaryOperation(tmpl, expr.op, tmpr).evaluate(None)
        elif isinstance(tmpl, model.Number) and isinstance(tmpr, model.Reference):
            if not tmpl.value:
                return model.Number(0)
        elif isinstance(tmpl, model.Reference) and isinstance(tmpr, model.Number):
            if not tmpr.value:
                return model.Number(0)
        elif isinstance(tmpl, model.Reference) and isinstance(tmpr, model.Reference) and expr.op == "-":
            if tmpl.name == tmpr.name:
                return model.Number(0)
            return model.BinaryOperation(tmpl, expr.op, tmpr)
            
    def visitNumber(self, extra):
        return extra
        
    def visitPrint(self, extra):
        return model.Print(extra.expr.visit(self))
        
    def visitRead(self, extra):
        return extra
        
    def visitReference(self, extra):
        return extra
        
    def visitFunctionDefinition(self, extra):
        return model.FunctionDefinition(extra.name, model.Function(extra.function.args, list(map(lambda x: x.visit(self), extra.function.body))))
    
    def visitFunctionCall(self, extra):
        return model.FunctionCall(extra.fun_expr.visit(self), list(map(lambda x: x.visit(self), extra.args)))
        
    def visitConditional(self, extra):
        return model.Conditional(extra.condition.visit(self), list(map(lambda x: x.visit(self), extra.if_true)), list(map(lambda x: x.visit(self), extra.if_false)))
    
    # -*- coding: utf-8 -*-
if __name__ == '__main__':
    pass
    """a = Scope()
    a["cond4"] = BinaryOperation(Number(5), '+', Number(8))
    c = ConstantFolder()
    a['cond4'] = c.visit(a['cond4'])"""