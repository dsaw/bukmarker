

import unittest,logging
import json
import sqlite3

from bukmarker import load_chrome_bookmarks,read_json_bookmarks,read_firefox_bookmarks_db, traverse_bm_folder
# TODO: need to write better tests!


class TestImports(unittest.TestCase):

    def setUp(self):
        self.chrome_bm = load_chrome_bookmarks(read_json_bookmarks())

    def tearDown(self):
        pass

    def test_traverse_folder(self):
        """

        :return:
        """

        bm_list = list()
        for bkey, bval in self.chrome_bm.items():

            if bval["type"] == "folder":
                print("Bookmark Folder - {0}".format(bkey))
                bm_list.extend(traverse_bm_folder(bval["children"], bval["name"]))
                for bm in traverse_bm_folder(bval["children"], bval["name"]):
                    print("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))

        self.assertGreater(len(bm_list),0)


    def test_firefox_import(self):
        """
        Test case for importing bookmarks from firefox places.sqlite file
        :return:
        """

        bm = read_firefox_bookmarks_db()
        self.assertGreater(len(bm), 0)


#temporary
if __name__ == "main":
    unittest.main(verbosity=2)

