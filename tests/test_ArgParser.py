import argparse
from bukmarker import create_parser,parse_args
import unittest


class ArgParserTest(unittest.TestCase):
    '''
    class to test the argument parser for bukmarker
    '''

    def setUp(self):
        self.parser = create_parser()


    def testAdd(self):
        '''

        :return:
        '''

        argv = ['--add','example.com','it\'an examples' ]
        ns = parse_args(argv)
        self.assertEqual(ns.add[0],'example.com')
        self.assertEqual(ns.add[1],'it\'an examples')





if __name__ == "main":
    unittest.main(verbosity=2)