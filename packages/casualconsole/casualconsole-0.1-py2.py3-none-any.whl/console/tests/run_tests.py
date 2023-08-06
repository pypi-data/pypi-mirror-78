import unittest

import console.tests.test_group as test_group

def create_suite():
  loader = unittest.TestLoader()
  test_suite = unittest.TestSuite()
  test_suite.addTest(loader.loadTestsFromModule(test_group))


  return test_suite

if __name__ == '__main__':
  suite = create_suite()
  runner = unittest.TextTestRunner()
  runner.run(suite)