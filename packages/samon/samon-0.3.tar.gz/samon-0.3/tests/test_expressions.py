from unittest import TestCase

from doculabs.samon.expressions import Bind, Condition, ForLoop


class ExpressionTest(TestCase):
    def test_bind_expression(self):
        b = Bind(expr='x * x')
        context = {'x': 2}
        self.assertEqual(b.eval(context=context), 4)

    def test_bind_expression_condition(self):
        b = Bind(expr='"big" if x > 100 else "small"')
        self.assertEqual(b.eval(context={'x': 2}), "small")
        self.assertEqual(b.eval(context={'x': 101}), "big")

    def test_condition(self):
        c = Condition(expr='x == 2')
        self.assertTrue(c.eval(context={'x': 2}))
        self.assertFalse(c.eval(context={'x': 3}))

        c = Condition(expr='True == False')
        self.assertFalse(c.eval(context={}))

    def test_looping(self):
        l = ForLoop(expr='c in it')
        context = {'it': ["a", "b", "c"]}
        iterable = l.eval(context=context)

        self.assertEqual(next(iterable), (1, 'c', "a"))
        self.assertEqual(next(iterable), (2, 'c', "b"))
        self.assertEqual(next(iterable), (3, 'c', "c"))

    def test_looping_naming_error(self):
        self.assertRaises(SyntaxError, lambda: ForLoop(expr='2 in it'))

        l = ForLoop(expr='a in b')
        context = {'c': 'asdf'}
        iterable = l.eval(context=context)
        self.assertRaises(ValueError, lambda: next(iterable))
