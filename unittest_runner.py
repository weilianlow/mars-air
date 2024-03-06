import xmlrunner
import unittest
import shutil
import os

if __name__ == '__main__':
    directory = 'unittest-results'
    path = os.path.join(os.getcwd(), directory)
    shutil.rmtree(path)
    suite = unittest.TestLoader().discover('.')
    runner = xmlrunner.XMLTestRunner(output=directory)
    runner.run(suite)