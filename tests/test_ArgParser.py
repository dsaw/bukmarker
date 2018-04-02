import argparse
from bukmarker import create_parser,parse_args
import unittest


class ArgParserTest(unittest.TestCase):
    '''
    class to test the argument parser for bukmarker
    '''

    def setUp(self):
        self.parser = create_parser()

    def test_add_tags(self):
        '''

        :return:
        '''

        argv = ['--add','example.com','it\'an examples' ]
        ns = parse_args(argv)
        self.assertEqual(ns.add[0],'example.com')
        self.assertEqual(ns.add[1],'it\'an examples')

    def test_search_tags(self):
        '''

        :return:
        '''
        argv = ['--search','--tags','+', 'bm', 'query']
        ns = parse_args(argv)
        self.assertListEqual(['+','bm','query'],ns.tags)
        self.assertEqual('?',ns.search)

    def test_append_tags(self):
        '''
        '''

        argv = ['--tags','larry','sergey','--append','www.google.com']
        ns = parse_args(argv)
        self.assertListEqual(['larry','sergey'],ns.tags)
        self.assertEqual('www.google.com',ns.append[0])

    def test_delete_tags(self):
        '''
        '''
        argv = ['--tags','larry','--delete']
        ns = parse_args(argv)
        self.assertEqual(['larry'],ns.tags)
        self.assertEqual('?',ns.delete)


    def test_export_bookmarks(self):
        '''

        :return:
        '''

        argv = ['--export','yama.html']
        ns = parse_args(argv)
        self.assertEqual('yama.html',ns.export)

    def test_auto_import(self):
        '''

        '''
        pass

if __name__ == "main":
    unittest.main(verbosity=2)