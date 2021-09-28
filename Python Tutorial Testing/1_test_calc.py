""" 
The TestCase class provides several assert methods to check for and report failures. The following table lists the most commonly used methods (see the tables below for more assert methods):

- assertEqual(a, b)
- assertNotEqual(a, b)
- assertTrue(x)
- assertFalse(x)
- assertIs(a, b)
- assertIsNot(a, b)
- assertIsNone(x)
- assertIsNotNone(x)
- assertIn(a, b)
- assertNotIn(a, b)
- assertIsInstance(a, b)
- assertNotIsInstance(a, b)
"""

import calc
import unittest

# create a class from unittest
class TestCalc(unittest.TestCase):

    # tests must start with "test_"
    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-10, 5), -5)
        self.assertEqual(calc.add(-1, -1), -2)
        self.assertEqual(calc.add(-5, 5), 0)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(-10, 5), -15)
        self.assertEqual(calc.subtract(-1, -1), 0)
        self.assertEqual(calc.subtract(-5, 5), -10)

    def test_multiply(self):
        self.assertEqual(calc.multiply(10, 5), 50)
        self.assertEqual(calc.multiply(-10, 5), -50)
        self.assertEqual(calc.multiply(-1, -1), 1)
        self.assertEqual(calc.multiply(-5, 0), 0)

    def test_divide(self):
        self.assertEqual(calc.divide(10, 5), 2)
        self.assertEqual(calc.divide(-10, 5), -2)
        self.assertEqual(calc.divide(-1, -1), 1)

        # catch // instead of /
        self.assertEqual(calc.divide(-5, 2), -2.5)

        # test exceptions
        self.assertRaises(ValueError, calc.divide, 1, 0)

        # test exceptions with context manager
        with self.assertRaises(ValueError):
            calc.divide(10, 0)


if __name__ == "__main__":
    unittest.main()
