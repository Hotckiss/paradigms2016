# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 00:23:04 2016

@author: Андрей
"""
import model
import printer
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
            if tmpl.value == 0:
                return model.Number(0)
        elif isinstance(tmpl, model.Reference) and isinstance(tmpr, model.Number):
            if tmpr.value == 0:
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
    
if __name__ == '__main__':
    pass
    """pr1 = printer.PrettyPrinter()
    a = model.Scope()
    a["ee"] = model.BinaryOperation(model.Number(5), "+", model.BinaryOperation(model.Number(6), "*", model.Number(7)))
    pr1.visit(a['ee'])
    a["foo"] = model.Function(('a1', 'a2',),
                             [model.Print(model.Reference('a1')), model.Print(model.Reference('a2'))])
    a['ttt'] = model.FunctionDefinition('foo', a['foo'])
    #pr1.visit(a['ttt'])
    a['rrr'] = model.FunctionCall(model.Reference('foo'),
                 [model.Number(5), model.Number(3)])
    a["cond3"] = model.Conditional(model.Reference('a1'), [model.Print(model.Number(5))], None)
    a["bazooka"] = model.Function(('a1', 'a2',),
                             [model.Print(model.Reference('a1')), model.Print(model.Reference('a2')),
                              model.Print(model.BinaryOperation(model.Reference('a1'), '+', model.Reference('a2'))),
                              model.Print(model.BinaryOperation(model.Reference('a1'), '-', (model.BinaryOperation(model.Reference('a1'), '-', model.Reference('a2'))))),
                              model.Print(model.UnaryOperation('-', model.Reference('a1'))),
                              model.Print(model.UnaryOperation('!', model.Reference('a1')))])
    pr1.visit(a['ee'])
    pr1.visit(a['rrr'])    
    pr1.visit(a['cond3'])
    pr1.visit(model.FunctionDefinition('bazooka', a['bazooka']))
    f1 = ConstantFolder()
    a["cond4"] = model.BinaryOperation(model.Number(0), '*', a['ee'])
    pr1.visit(a['cond4'])
    a['cond4'] = f1.visit(a['cond4'])
    pr1.visit(a['cond4'])"""