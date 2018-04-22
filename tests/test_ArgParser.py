import argparse
from bukmarker import create_parser,parse_args
import unittest


class ArgParserTest(unittest.TestCase):
    '''
    class to test the argument parser for bukmarker
    '''

    def setUp(self):
        self.parser = create_parser()

    def test_delete(self):
        '''
        Check url of delete is correct
        :return:
        '''
        argv = ['--delete', 'example.com']
        ns = parse_args(argv)
        self.assertEqual(ns.delete,'example.com')

    def test_search(self):
        '''
        Check url of search is correct
        :return:
        '''

        argv = ['--search','exam.com']
        ns = parse_args(argv)
        self.assertEqual(ns.search, 'exam.com')

    def test_add_tags(self):
        '''

        :return:
        '''

        argv = ['--add','example.com','--title','it\'an','examples' ]
        ns = parse_args(argv)
        self.assertEqual(ns.add,'example.com')
        self.assertEqual(ns.title[1],'examples')

    def test_modify_tags_with_options(self):
        '''

        :return:
        '''
        argv = ['--modify','example.com','--title','new','example', '--desc', 'Just','kidding' ]
        ns = parse_args(argv)
        self.assertEqual(ns.modify, 'example.com')
        self.assertEqual(ns.title[0], 'new')
        self.assertEqual(ns.desc[1],'kidding')

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
        self.assertEqual('www.google.com',ns.append)

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
        argv = ['--ai', '-ai']
        ns = parse_args(argv)
        self.assertTrue(ns.ai)

    def test_export(self):
        '''

        :return:
        '''
        argv = ['--export','yesman.html','--ai']
        ns = parse_args(argv)
        self.assertTrue(ns.ai)
        self.assertEqual('yesman.html',ns.export)

    def test_failing_exp(self):
        '''
        test unrecognized arguments which should fail
        :return:
        '''

        with self.assertRaises(SystemExit):
            argv = ['--expot', '--ai']
            ns = parse_args(argv)
        #self.assertEqual('',ns.export)



if __name__ == "main":
    unittest.main(verbosity=2)