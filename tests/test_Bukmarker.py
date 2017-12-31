

import unittest
import os
import logging
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

    def test_add_duplicate_bookmark(self):
        """
        Adds a bookmark with same url.
        Test passes if -1 is returned
        :return:
        """
        self.bukmarker.add_bookmark_db('www.google.com')
        ret = self.bukmarker.add_bookmark_db('www.google.com')
        self.assertEqual(ret,-1)

    def test_deletion_bookmark(self):
        """
        Deletes a bookmark with given url
        :return:
        """
        self.bukmarker.add_bookmark_db('www.google.com')
        ret = self.bukmarker.delete_bookmark_db('www.google.com')
        self.assertEqual(ret,'www.google.com')

    def test_modify_all_param_bookmark(self):
        """
        Modify a bookmark
        :return:
        """
        ret = self.bukmarker.modify_bookmark_db("www.google.com","The search engine of the internet","search,google,query","No description required")
        self.assertEqual(ret,"www.google.com")

    def test_modify_title_bookmark(self):
        """
        Modify only title
        :return:
        """
        ret = self.bukmarker.modify_bookmark_db("www.google.com", "Googleplex")
        self.assertEqual(ret, "www.google.com")

    def test_modify_fetch_title(self):
        """
        Pass in url only and fetch title automatically
        :return:
        """
        ret = self.bukmarker.modify_bookmark_db("www.google.com")
        self.assertEqual(ret,"www.google.com")

    def test_fetch_title_bookmark(self):
        """
        tests fetching action
        :return:
        """
        actual_title = "Example Domain"
        fetched_title = self.bukmarker.fetch_title_bookmark('http://example.com/')
        self.assertEqual(fetched_title,actual_title)

    def test_fetch_title_not_found(self):
        """
        tests by fetching from non-existent host.
        :return:
        """
        non_existent_domain = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/de"
        with self.assertLogs("bukmarker.py",level="ERROR") as cm:
            ret = self.bukmarker.fetch_title_bookmark(non_existent_domain)
        ## TODO: check whether error is 404

    def test_append_tags(self):
        """
        tests by appending arbitrary tags.
        :return:
        """

        new_tags = ["google","larry","sergey"]

        ret = self.bukmarker.append_tags("www.google.com",new_tags)
        ## TODO: use get_tags to check
        self.assertEqual(ret,"www.google.com")

    def test_delete_tags(self):
        """
        tests by deleting tags
        :return:
        """
        tags_to_delete = "google,larry,sergey"
        ret = self.bukmarker.delete_tags("www.google.com",tags_to_delete)
        self.assertEqual(ret,"www.google.com")


    def test_delete_first_last_tag(self):
        """

        :return:
        """
        pass

    def test_search_by_url(self):
        """
        Tests if bookmark with url exists

        """
        ret = self.bukmarker.search_by_url("www.google.com")
        self.assertEquals(ret['url'],'www.google.com')
        self.bukmarker.print_rec(ret)

    def test_parse_tags(self):
        """
        Tests if the tag list is cleaned and joined
        :return:
        """

        tag_list = ["seo ", "google ","dark   ",   "seo", "   dark"]
        ret_str = self.bukmarker.parse_tags(tag_list)
        self.assertEqual(ret_str,"dark,google,seo")


#temporary
if __name__ == "main":

    unittest.main(verbosity=2)

