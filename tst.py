import unittest
from unittest.mock import patch
from io import StringIO
from model import *

class Scope_Test(unittest.TestCase):
    def test_base_dict(self):
        s = Scope()
        s['qqqq'] = 1234567
        s['bar'] = 100500
        s['foo'] = 322
        s['bazooka'] = 5553535
        s['hard_testing'] = 30
        self.assertEqual(s['qqqq'], 1234567)
        self.assertEqual(s['bar'], 100500)
        self.assertEqual(s['foo'], 322)
        self.assertEqual(s['bazooka'], 5553535)
        self.assertEqual(s['hard_testing'], 30)
    def test_first_ancestor(self):
        s = Scope()
        sa = Scope(s)
        s['fa'] = 1
        s['gunner'] = 101010
        self.assertEqual(sa['fa'], 1)
        self.assertEqual(sa['gunner'], 101010)
    def test_higher_ancestor(self):
        s = Scope()
        sa = Scope(s)
        ssa = Scope(sa)
        s['fa'] = 1
        s['gunner'] = 101010
        self.assertEqual(ssa['fa'], 1)
        self.assertEqual(ssa['gunner'], 101010)
    def test_priority(self):
        s = Scope()
        sa = Scope(s)
        s['gunner'] = 1
        sa['gunner'] = 10
        self.assertEqual(sa['gunner'], 10)
    def test_hard_testing(self):
        s = Scope()
        ss = Scope(s)
        sss = Scope(ss)
        ssp = Scope(ss)
        s['a'] = 1
        ss['a'] = 2
        sss['a'] = 3
        s['b'] = 4
        ssp['gg'] = 5
        self.assertEqual(sss['a'], 3)
        self.assertEqual(ss['a'], 2)
        self.assertEqual(s['a'], 1)
        self.assertEqual(ssp['a'], 2)
        self.assertEqual(ssp['gg'], 5)
        self.assertEqual(s['b'], 4)
        self.assertEqual(ss['b'], 4)
        self.assertEqual(sss['b'], 4)
        self.assertEqual(ssp['b'], 4)
    def test_triple_tree_two_level(self):
        root = Scope()
        a1 = Scope(root)
        a2 = Scope(root)
        a3 = Scope(root)
        a11 = Scope(a1)
        a12 = Scope(a1)
        a13 = Scope(a1)
        a21 = Scope(a2)
        a22 = Scope(a2)
        a23 = Scope(a2)
        a31 = Scope(a3)
        a32 = Scope(a3)
        a33 = Scope(a3)
        root['a'] = 7
        a1['a'] = 77
        a21['a'] = 777
        self.assertEqual(root['a'], 7)
        self.assertEqual(a1['a'], 77)
        self.assertEqual(a2['a'], 7)
        self.assertEqual(a3['a'], 7)
        self.assertEqual(a11['a'], 77)
        self.assertEqual(a12['a'], 77)
        self.assertEqual(a13['a'], 77)
        self.assertEqual(a21['a'], 777)
        self.assertEqual(a22['a'], 7)
        self.assertEqual(a23['a'], 7)
        self.assertEqual(a31['a'], 7)
        self.assertEqual(a32['a'], 7)
        self.assertEqual(a33['a'], 7)
        
class Number_Test(unittest.TestCase):
    def test_typ(self):
        a = Scope()
        a['viking'] = Number(777)
        a['non'] = Number(0)
        a['otr'] = Number(-7)
        self.assertIsInstance(a['viking'], Number)
        self.assertIsInstance(a['non'], Number)
        self.assertIsInstance(a['otr'], Number)
        self.assertIsInstance(a['viking'].evaluate(a), Number)
        self.assertIsInstance(a['non'].evaluate(a), Number)
        self.assertIsInstance(a['otr'].evaluate(a), Number)
        
class Reference_Test(unittest.TestCase):
    def test_all(self):
        s = Scope()
        s['q'] = Number(-2)
        s['w'] = Number(-1)
        s['e'] = Number(0)
        s['r'] = Number(1)
        s['t'] = Number(2)
        s['y'] = Number(3)
        a = Reference('q')
        self.assertIs(a.evaluate(s), s['q'])
        b = Reference('w')
        self.assertIs(b.evaluate(s), s['w'])
        a = Reference('w')
        self.assertIs(a.evaluate(s), s['w'])
        a = Reference('e')
        self.assertIs(a.evaluate(s), s['e'])
        a = Reference('y')
        self.assertIs(a.evaluate(s), s['y'])
        #s['y'] = 333
        #self.assertIs(a.evaluate(s), 333)

class Function_Test(unittest.TestCase):
    def test_typ(self):
        a = Scope()
        a['q'] = Function(['wat'], [Number(5553535), Number(35)])
        self.assertIsInstance(a['q'].evaluate(a), Number)
        self.assertIsInstance(a['q'], Function)
    def test_eval_ne_ne(self):
        with patch('sys.stdout', new_callable = StringIO) as cout:
            a = Scope()
            a['q'] = Function(['wat'], [Number(5553535), Number(35)])
            Print(a['q'].evaluate(a)).evaluate(a)
            self.assertEqual(cout.getvalue(), str(35) + '\n')
    def test_eval_ne_e(self):
        a = Scope()
        a['q1'] = Function(['wat1'], [])
        #self.assertIs(1, 1)
    """def test_eval_e_ne(self):
        a = Scope()
        a['q2'] = Function([], [Number(5553535), Number(35)])
        #self.assertIs(a['q2'].evaluate(a).value, 35)"""
    """def test_eval_e_e(self):
        a = Scope()
        a['q3'] = Function([], [])
        self.assertIs(1, 1)"""
          
class Fdef_Test(unittest.TestCase):
    def test_fdef(self):
        a = Scope()
        f = Function(['i_love_yat'], [Number(5553535), Number(35)])
        fdef = FunctionDefinition('my_super_puper_func', f)
        self.assertIsInstance(fdef.evaluate(a), Function)
        self.assertIsInstance(a['my_super_puper_func'], Function)
        self.assertIs(a['my_super_puper_func'], f)
    def test_fdef_empt(self):
        a = Scope()
        f = Function(['i_love_yat'], [])
        fdef = FunctionDefinition('my_super_puper_func', f)
        self.assertIsInstance(fdef.evaluate(a), Function)
        self.assertIsInstance(a['my_super_puper_func'], Function)
        self.assertIs(a['my_super_puper_func'], f)

class Fcall_Test(unittest.TestCase):
    def test_ffull(self):
        with patch('sys.stdout', new_callable = StringIO) as cout:
            a = Scope()
            f = Function(['i_love_yat', 'br'], [Reference('i_love_yat'), Reference('br')])
            fd = FunctionDefinition('my_super_puper_func', f)
            fc = FunctionCall(fd, [Number(5553535), Number(35)])
            self.assertIsInstance(fc.evaluate(a), Number)
            Print(fc.evaluate(a)).evaluate(a)
            self.assertEqual(cout.getvalue(), str(35) + '\n')
            #self.assertIs(fc.evaluate(a).value, 35)
    def test_fempt(self):
        a = Scope()
        f = Function(['i_love_yat', 'br'], [])
        fd = FunctionDefinition('my_super_puper_func', f)
        fc = FunctionCall(fd, [Number(5553535), Number(35)])
        fc.evaluate(a)

class Cond_Test(unittest.TestCase): # 1 - full list 2 - empty list 3 - None list
    def setUp(self):
        self.s = Scope()
        self.t = Number(1)
        self.f = Number(0)
    def test_true_1_1(self):
        with patch('sys.stdout', new_callable = StringIO) as cout:
            c = Conditional(self.t, [Number(1), Number(2)], [Number(3), Number(4)])
            Print(c.evaluate(self.s)).evaluate(self.s)
            self.assertEqual(cout.getvalue(), str(2) + '\n')
            #self.assertIs(c.evaluate(self.s).value, 2)
    """def test_true_1_2(self):
        c = Conditional(self.t, [Number(1), Number(2)], [])
        self.assertIs(c.evaluate(self.s).value, 2)
    def test_true_1_3(self):
        c = Conditional(self.t, [Number(1), Number(2)], None)
        self.assertIs(c.evaluate(self.s).value, 2)
    def test_true_2_1(self):
        c = Conditional(self.t, [], [Number(3), Number(4)])
        c.evaluate(self.s)"""
    def test_true_2_2(self):
        c = Conditional(self.t, [], [])
        c.evaluate(self.s)
    """def test_true_2_3(self):
        c = Conditional(self.t, [], None)
        c.evaluate(self.s)
    def test_true_3_1(self):
        c = Conditional(self.t, None, [Number(3), Number(4)])
        c.evaluate(self.s)
    def test_true_3_2(self):
        c = Conditional(self.t, None, [])
        c.evaluate(self.s)"""
    def test_true_3_3(self):
        c = Conditional(self.t, None, None)
        c.evaluate(self.s)
    """def test_false_1_1(self):
        c = Conditional(self.f, [Number(1), Number(2)], [Number(3), Number(4)])
        self.assertIs(c.evaluate(self.s).value, 4)
    def test_false_1_2(self):
        c = Conditional(self.f, [Number(1), Number(2)], [])
        c.evaluate(self.s)
    def test_false_1_3(self):
        c = Conditional(self.f, [Number(1), Number(2)], None)
        c.evaluate(self.s)
    def test_false_2_1(self):
        c = Conditional(self.f, [], [Number(3), Number(4)])
        self.assertIs(c.evaluate(self.s).value, 4)
    def test_false_2_2(self):
        c = Conditional(self.f, [], [])
        c.evaluate(self.s)
    def test_false_2_3(self):
        c = Conditional(self.f, [], None)
        c.evaluate(self.s)
    def test_false_3_1(self):
        c = Conditional(self.f, None, [Number(3), Number(4)])
        self.assertIs(c.evaluate(self.s).value, 4)
    def test_false_3_2(self):
        c = Conditional(self.f, None, [])
        c.evaluate(self.s)
    def test_false_3_3(self):
        c = Conditional(self.f, None, None)
        c.evaluate(self.s)"""

class Read_Test(unittest.TestCase):
    def test_read(self):
        for i in range(-30, 239):
            with patch('sys.stdin', new = StringIO(str(i) + '\n')), patch('sys.stdout', new_callable = StringIO) as cout:
                a = Scope()
                num = Read('wat').evaluate(a)
                self.assertIsInstance(num, Number)
                Print(num).evaluate(a)
                self.assertEqual(cout.getvalue(), str(i) + '\n')

class Print_Test(unittest.TestCase):
    def test_print_1(self):
        for i in range(-30, 239):
            with patch('sys.stdout', new_callable = StringIO) as cout:
                a = Scope()
                Print(Number(i)).evaluate(a)
                self.assertEqual(cout.getvalue(), str(i) + '\n')
    def test_print_2(self):
        for i in range(-30, 239):
            with patch('sys.stdout', new_callable = StringIO) as cout:
                a = Scope()
                a[str(i + 70)] = Number(i)
                Print(Reference(str(i + 70))).evaluate(a)
                self.assertEqual(cout.getvalue(), str(i) + '\n')

class Binary_Test(unittest.TestCase):
    def test_binary(self):
        a = Scope()
        dct = ['+', '-', '*', '/', '%', '&&', '||', '==', '!=', '<', '>', '<=', '>=']
        for l in range(-30, 23):
            for r in range(-29, 30):
                for op in dct:
                    if r == 0 and (op == '/' or op == '%'):
                       continue
                    with patch('sys.stdout', new_callable = StringIO) as cout:
                        val = BinaryOperation(Number(l), op, Number(r)).evaluate(a)
                        Print(val).evaluate(a)
                        if op == '+':
                            self.assertEqual(cout.getvalue(), str(l + r) + '\n')
                        elif op == '-':
                            self.assertEqual(cout.getvalue(), str(l - r) + '\n')
                        elif op == '*':
                            self.assertEqual(cout.getvalue(), str(l * r) + '\n')
                        elif op == '/':
                            self.assertEqual(cout.getvalue(), str(l // r) + '\n')
                        elif op == '%':
                            self.assertEqual(cout.getvalue(),str(l % r) + '\n')
                        elif op == '&&':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l and r))
                        elif op == '||':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l or r))
                        elif op == '==':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l == r))
                        elif op == '!=':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l != r))
                        elif op == '<':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l < r))
                        elif op == '>':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l > r))
                        elif op == '<=':
                            self.assertEqual(bool(int(cout.getvalue())), bool(l <= r))
                        else:
                            self.assertEqual(bool(int(cout.getvalue())), bool(l >= r))
                        
class Unary_Test(unittest.TestCase):
    def test_unary(self):
        a = Scope()
        dct = ['-', '!']
        for n in range(-30, 239):
            for op in dct:
                with patch('sys.stdout', new_callable = StringIO) as cout:
                    val = UnaryOperation(op, Number(n)).evaluate(a)
                    Print(val).evaluate(a)
                    if op == '-':
                        self.assertEqual(cout.getvalue(), str(-n) + '\n')
                    else:
                        self.assertNotEqual(bool(int(cout.getvalue())), bool(n))
if __name__ == '__main__':
    unittest.main()
