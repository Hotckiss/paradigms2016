import yat.model
import yat.printer
class ConstantFolder:
    def visit(self, tree):
        return tree.visit(self)
    def listev(self, expr):
        if expr is not None:
            return [x.visit(self) for x in expr]
        else:
            return None
    def visitUnaryOperation(self, expr):
        tmp = expr.expr.visit(self)
        if isinstance(tmp, yat.model.Number):
            return yat.model.UnaryOperation(expr.op, tmp).evaluate(None)
        return yat.model.UnaryOperation(expr.op, tmp)
    def visitBinaryOperation(self, expr):
        tmpl = expr.lhs.visit(self)
        tmpr = expr.rhs.visit(self)
        if isinstance(tmpl, yat.model.Number) and isinstance(tmpr, yat.model.Number):
            return yat.model.BinaryOperation(tmpl, expr.op, tmpr).evaluate(None)
        elif isinstance(tmpl, yat.model.Number) and isinstance(tmpr, yat.model.Reference):
            if tmpl.value == 0:
                return yat.model.Number(0)
        elif isinstance(tmpl, yat.model.Reference) and isinstance(tmpr, yat.model.Number):
            if tmpr.value == 0:
                return yat.model.Number(0)
        elif isinstance(tmpl, yat.model.Reference) and isinstance(tmpr, yat.model.Reference) and expr.op == "-":
            if tmpl.name == tmpr.name:
                return yat.model.Number(0)
        return yat.model.BinaryOperation(tmpl, expr.op, tmpr)
            
    def visitNumber(self, extra):
        return extra
        
    def visitPrint(self, extra):
        return yat.model.Print(extra.expr.visit(self))
        
    def visitRead(self, extra):
        return extra
        
    def visitReference(self, extra):
        return extra
        
    def visitFunctionDefinition(self, extra):
        return yat.model.FunctionDefinition(extra.name, yat.model.Function(extra.function.args, self.listev(extra.function.body)))
    
    def visitFunctionCall(self, extra):
        return yat.model.FunctionCall(extra.fun_expr.visit(self), self.listev(extra.args))
        
    def visitConditional(self, extra):
        return model.Conditional(extra.condition.visit(self), self.listev(extra.if_true), self.listev(extra.if_false) if extra.if_false is not None else None)
    
if __name__ == '__main__':
    pass
    """pr1 = yat.printer.PrettyPrinter()
    a = yat.model.Scope()
    a["ee"] = yat.model.BinaryOperation(yat.model.Number(5), "+", yat.model.BinaryOperation(yat.model.Number(6), "*", yat.model.Number(7)))
    pr1.visit(a['ee'])
    a["foo"] = yat.model.Function(('a1', 'a2',),
                             [yat.model.Print(yat.model.Reference('a1')), yat.model.Print(yat.model.Reference('a2'))])
    a['ttt'] = yat.model.FunctionDefinition('foo', a['foo'])
    #pr1.visit(a['ttt'])
    a['rrr'] = yat.model.FunctionCall(yat.model.Reference('foo'),
                 [yat.model.Number(5), yat.model.Number(3)])
    a["cond3"] = yat.model.Conditional(yat.model.Reference('a1'), [yat.model.Print(yat.model.Number(5))], [yat.model.Print(yat.model.Number(5))])
    a["bazooka"] = yat.model.Function(('a1', 'a2',),
                             [yat.model.Print(yat.model.Reference('a1')), yat.model.Print(yat.model.Reference('a2')),
                              yat.model.Print(yat.model.BinaryOperation(yat.model.Reference('a1'), '+', yat.model.Reference('a2'))),
                              yat.model.Print(yat.model.BinaryOperation(yat.model.Reference('a1'), '-', (yat.model.BinaryOperation(yat.model.Reference('a1'), '-', yat.model.Reference('a2'))))),
                              yat.model.Print(yat.model.UnaryOperation('-', yat.model.Reference('a1'))),
                              yat.model.Print(yat.model.UnaryOperation('!', yat.model.Reference('a1')))])
    pr1.visit(a['ee'])
    pr1.visit(a['rrr'])    
    pr1.visit(a['cond3'])
    pr1.visit(yat.model.FunctionDefinition('bazooka', a['bazooka']))
    f1 = ConstantFolder()
    a["cond4"] = yat.model.BinaryOperation(yat.model.Number(0), '*', a['ee'])
    pr1.visit(a['cond4'])
    a['cond4'] = f1.visit(a['cond4'])
    pr1.visit(a['cond4'])
    number = yat.model.Number(42)
    pp = yat.model.Print(number)
    pr1.visit(pp)"""
