

import unittest
import json
import sqlite3

from bukmarker import load_chrome_bookmarks,read_json_bookmarks,traverse_bm_folder

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

#temporary
if __name__ == "main":
    unittest.main(verbosity=2)

