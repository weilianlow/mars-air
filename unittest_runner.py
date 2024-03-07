import xmlrunner
import unittest

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('.')
    runner = xmlrunner.XMLTestRunner(output='unittest-results')
    runner.run(suite)