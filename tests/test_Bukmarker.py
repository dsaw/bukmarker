

import unittest,os,logging
#logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)
import json
import sqlite3

import bukmarker
# TODO: need to write better tests!


class TestImports(unittest.TestCase):

    def setUp(self):
        # relative logfile path
        self.bukmarker = bukmarker.BukmarkerDB()
        logfile_path = os.path.abspath(os.path.dirname(os.path.__file__))
        logfilename = os.path.join(logfile_path, "..\bukmarker.log")
        self.chrome_bm = self.bukmarker.load_chrome_bookmarks(self.bukmarker.read_json_bookmarks())
        logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)

    def tearDown(self):
        pass

    def test_traverse_folder(self):
        """

        :return:
        """

        bm_list = list()
        for bkey, bval in self.chrome_bm.items():                  # TODO : refactor traverse folder to bukmarker class
            if bval["type"] == "folder":
                logging.info("Bookmark Folder - {0}".format(bkey))
                bm_list.extend(self.bukmarker.traverse_bm_folder(bval["children"], bval["name"]))
                for bm in self.bukmarker.traverse_bm_folder(bval["children"], bval["name"]):
                    logging.debug("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))

        self.assertGreater(len(bm_list),0)

    def test_firefox_import(self):
        """
        Test case for importing bookmarks from firefox places.sqlite file
        :return:
        """

        bm = self.bukmarker.read_firefox_bookmarks_db()
        self.assertGreater(len(bm), 0)

    def test_dbfile_windows(self):
        """
        Test case for checking windows database directory
        :return:
        """
        dbfile = bukmarker.BukmarkerDB.get_default_dbdir()

        self.assertEqual(dbfile,"C:\\Users\\Devesh\\AppData\\Roaming\\bukmarker.sqlite")

    def test_bookmark_table_creation(self):
        """
        Test case for checking creation of new table
        :return:
        """

        self.bukmarker.create_bookmark_db()

    def test_bookmark_table_file_not_found(self):
        """
        Test by opening a non existent db file
        :return:
        """

        self.bukmarker.dbfile = "C:\\Users\\Devesh\\AppData\\Roaming\\buk"
        self.bukmarker.create_bookmark_db()
        self.assertRaises(sqlite3.OperationalError)

    def test_adding_duplicate_bookmark(self):
        """
        Adds a bookmark with same url.
        Test passes if exception raised
        :return:
        """
        with self.assertRaises(sqlite3.DatabaseError):
            self.bukmarker.add_bookmark_db('www.google.com')

#temporary
if __name__ == "main":

    unittest.main(verbosity=2)

