import unittest
from functions_ext import optimizer, isQuadrangle


class TestOptimizer(unittest.TestCase):
    def test_optimizerWithValidInput(self):
        a, b, c, d = 5, 6, 10, 12
        teta2start, teta2end = 0, 90
        configuration, omega, epsilon = optimizer(a, b, c, d, teta2start, teta2end)
        self.assertEqual([a, b, c, d, 90, 75.2], configuration)

    def test_optimizerWithInvalidInput(self):
        a, b, c, d = 5, 6, 10, 25
        teta2start, teta2end = 0, 90
        configuration, omega, epsilon = optimizer(a, b, c, d, teta2start, teta2end)
        self.assertEqual([], configuration)


class TestIsQuadrangle(unittest.TestCase):
    def test_isQuadrangle(self):
        values = ((12, True),
                  (25, False))
        a, b, c = 5, 6, 7
        for d, expRes in values:
            res = isQuadrangle(a, b, c, d)
            self.assertEqual(expRes, res)


if __name__ == '__main__':
    unittest.main()
