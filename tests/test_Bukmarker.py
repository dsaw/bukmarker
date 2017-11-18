

import unittest,logging,os
#logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)
import json
import sqlite3

import bukmarker
# TODO: need to write better tests!


class TestImports(unittest.TestCase):

    def setUp(self):
        # relative logfile path
        self.bukmarker = bukmarker.BukmarkerDB("conn","cursor")
        logfile_path = os.path.abspath(os.path.dirname(os.path.__file__))
        logfilename = os.path.join(logfile_path, "..\bukmarker.log")
        self.chrome_bm = self.bukmarker.load_chrome_bookmarks(self.bukmarker.read_json_bookmarks())
        logging.basicConfig(filename=logfilename,filemode="w", level=logging.BASIC_FORMAT)

    def tearDown(self):
        pass

    def test_traverse_folder(self):
        """

        :return:
        """

        bm_list = list()
        for bkey, bval in self.chrome_bm.items():
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

        self.assertEqual(dbfile,"C:\\Users\\Devesh\\AppData\\Roaming\\buku")

#temporary
if __name__ == "main":

    unittest.main(verbosity=2)

