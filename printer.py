def bread(func):
    def wrapper(self, arg):
        print("(", end = '')
        func(self, arg)
        print(")", end = '')
    return wrapper
class PrettyPrinter():
    def __init__(self):
        self.spaces = 0
        
    def visit(self, expr):
        expr.visit(self)
        print(";")
    def put(self, expr):
        self.spaces += 1
        for stat in expr:
            print("    " * self.spaces, end = '')
            stat.visit(self)
            print(";")
        self.spaces -= 1
        
    def visitNumber(self, num):
        print(num.value, end='')
        
    def visitPrint(self, p):
        print("print ", end='')
        p.expr.visit(self)
        
    def visitRead(self, r):
        print("read " + r.name, end='')
        
    def visitReference(self, rf):
        print(rf.name, end='')
    
    def visitFunctionDefinition(self, fdef):
        print("def ", end = '')
        print(fdef.name, end = '')
        print("(", end = '')
        print(", ".join(fdef.function.args), end = '')
        print(") {")
        self.put(fdef.function.body)
        print("    " * self.spaces + "}", end = '')
        
    def visitFunctionCall(self, call):
        call.fun_expr.visit(self)
        print("(", end = '')
        is_first = 1
        for arg in call.args:
            if not is_first:
                print(',', end=' ')
            arg.visit(self)
            is_first = 0
        print(")", end='')
    def visitConditional(self, cond):
        print("if (", end = '')
        cond.condition.visit(self)
        print(") {")
        if cond.if_true:
            self.put(cond.if_true)
        print("    " * self.spaces + "}")
        if cond.if_false == None:
            print("{}", end ='')
        else:
            print(" else {")    
            self.put(cond.if_false)
            print("    " * self.spaces + "}", end='')
    @bread
    def visitBinaryOperation(self, expr):
        expr.lhs.visit(self)
        print(" " + expr.op, end=' ')
        expr.rhs.visit(self)
    @bread
    def visitUnaryOperation(self, expr):
        print(expr.op, end ='')
        expr.expr.visit(self)

        
        
