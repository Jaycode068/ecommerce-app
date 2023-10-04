import unittest
from tests import test_auth

if __name__ == "__main__":
    # Add your test modules here
    test_modules = [test_auth]

    # Create the test suite
    test_suite = unittest.TestSuite()

    for test_module in test_modules:
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_module))

    # Run the tests
    unittest.TextTestRunner(verbosity=2).run(test_suite)
