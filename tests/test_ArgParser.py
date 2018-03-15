import argparse
import bukmarker
import unittest




class ArgParserTest(unittest.TestCase):
    '''
    class to test the argument parser for bukmarker
    '''

    def setUp(self):
        self.parser = create_parser()

