import os
import shutil
from unittest import TestCase

from capsules.capsules import capsules

# Remove directory if it exists to ensure
# tests have full coverage.
if os.path.exists('./__capsules__'):
    shutil.rmtree('./__capsules__')

# Definitions of functions used in unit tests.
global identity
identity = lambda x: x

global double
@capsules
def double(x):
    return x + x

global square
def square(x):
    return x * x

global power
exec('def power(x): return x**x')

class Test_capsules(TestCase):
    def test_non_function(self):
        self.assertRaises(TypeError, capsules, 123)
        try:
            capsules(123)
            self.assertFail()
        except TypeError as error:
            self.assertEqual(str(error), 'input is not a function')

    def test_lambda(self):
        global identity
        self.assertRaises(ValueError, capsules, identity)
        try:
            capsules(identity)
            self.assertFail()
        except ValueError as error:
            self.assertEqual(str(error), 'lambda functions are not supported')

    def test_no_source(self):
        global power
        self.assertRaises(OSError, capsules, power)
        try:
            capsules(power)
            self.assertFail()
        except OSError as error:
            self.assertEqual(str(error), 'could not get source code')

    def test_decorator(self):
        global double
        self.assertTrue(double(2) == 4)

    def test_direct(self):
        global square
        square = capsules(square)
        self.assertTrue(square(3) == 9)
