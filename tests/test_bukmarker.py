

import unittest
import os
import logging
#logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)
import json
import sqlite3
import sys

import bukmarker
# TODO: need to write better tests!


class TestImports(unittest.TestCase):

    def setUp(self):
        # relative logfile path
        self.bukmarker = bukmarker.BukmarkerDB()
        self.bukmarker.create_bookmark_db()
        logfile_path = os.path.abspath(os.path.dirname(os.path.__file__))
        logfilename = os.path.join(logfile_path, "..\bukmarker.log")
        bm_json = {
            "checksum": "16b461a69b7d68e934ab650b6d0fb647",
            "roots": {
                "bookmark_bar": {
                    "children": [
                        {
                            "date_added": "13126525897558343",
                            "id": "68",
                            "meta_info": {
                                "last_visited_desktop": "13168927771220185"
                            },
                            "name": "Technology Archives - Five Books",
                            "type": "url",
                            "url": "http://fivebooks.com/tag/technology/"
                        },
                        { "children": [ {
                            "date_added": "13129454063033048",
                             "id": "129",
                             "meta_info": {
                                "last_visited_desktop": "13153436950213097"
                                },
                            "name": "Excess XSS: A comprehensive tutorial on cross-site scripting",
                            "type": "url",
                            "url": "https://excess-xss.com/"
            }, {
               "date_added": "13128973125269871",
               "id": "114",
               "meta_info": {
                  "last_visited_desktop": "13153484724895511"
               },
               "name": "Cracking 12 Character & Above Passwords",
               "type": "url",
               "url": "http://www.netmux.com/blog/cracking-12-character-above-passwords"
            }],
                        "date_added": "13129454086976852",
                        "date_modified": "13160843857449902",
                        "id": "130",
                        "name": "security_hackers",
                        "type": "folder"
                        }
                    ],

                    "date_added": "13120993414684871",
                    "date_modified": "13166367764503473",
                    "id": "1",
                    "name": "Bookmarks bar",
                    "type": "folder"
                }
            }

        }

        self.chrome_bm = self.bukmarker.ret_chrome_bookmarks(bm_json)
        logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)

        # testing bookmark
        if self.bukmarker.search_by_url("www.whothat.com") == -1:
            self.bukmarker.add_bookmark_db("www.whothat.com")

        if self.bukmarker.search_by_url("www.google.com") == -1:
            self.bukmarker.add_bookmark_db("www.google.com",tags="search,pagerank")

        if self.bukmarker.search_by_url("www.digg.com") == -1:
            self.bukmarker.add_bookmark_db("www.digg.com",title="Front page bookmarks" ,tags="bm,pagerank")

    def tearDown(self):
        self.bukmarker.close()
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

        self.assertEqual(len(bm_list),3)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_chrome_import(self):
        """
        Test case for importing bookmarks from chrome
        """

        count_entries = self.bukmarker.load_chrome_bookmarks()
        self.assertGreater(count_entries, 0)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_firefox_import(self):
        """
        Test case for importing bookmarks from firefox places.sqlite file
        :return:
        """
        bm = self.bukmarker.read_firefox_bookmarks_db()
        self.assertGreater(len(bm), 0)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
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
        self.bukmarker.add_bookmark_db('www.google.com')

    def test_modify_all_param_bookmark(self):
        """
        Modify a bookmark
        :return:
        """
        ret = self.bukmarker.modify_bookmark_db("www.whothat.com","The address book everyone wants","whois,identity","No description required")
        self.assertEqual(ret,"www.whothat.com")

    def test_modify_title_bookmark(self):
        """
        Modify only title
        :return:
        """
        ret = self.bukmarker.modify_bookmark_db("www.google.com", "Googleplex",tags_in="search,pagerank")
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
        self.assertNotEqual(ret,-1)
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

    def test_prep_tags(self):
        """"
        Tests if the prepping tag list func is working properly
        """

        tags_str1 = ['+','a','b','b','c']
        tags_str2 = ", ant aunt ars anderson".split(' ')
        tags_str3 = ", an + 2".split(' ')

        self.assertEqual('+',self.bukmarker.prep_tags(tags_str1)[1])
        self.assertEqual(',', self.bukmarker.prep_tags(tags_str2)[1])
        self.assertEqual(-1, self.bukmarker.prep_tags(tags_str3))

    def test_search_tags(self):
        """
        Tests if the tags are searched correctly

        """
        mock_or_tags = [',','search','bm']
        mock_and_tags = ['+','pagerank','search']
        retor = self.bukmarker.search_by_tags(mock_or_tags)
        retand = self.bukmarker.search_by_tags(mock_and_tags)
        self.assertEqual(2,len(retor))
        self.assertEqual("www.google.com",retand[0][0])

    def test_export_html(self):
        '''
        Tests if the html generated file has the correct no. of bookmarks
        :return:
        '''

        filename = 'bukmarker.html'
        exported_count = self.bukmarker.exportdb(filename)
        count = self.bukmarker.count_bookmarks
        self.assertEqual(count,exported_count)


    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_firefox_profile_subfolders(self):
        '''
        '''
        main_ff_profile_dir = "C:\\Users\\Devesh\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\x94qotzr.default-1509035816333"
        ret_prof_dir = bukmarker.get_firefox_profile_dir("C:\\Users\\Devesh\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\")

        self.assertEqual(ret_prof_dir,main_ff_profile_dir)


    @unittest.skip("Not decided what to do yet")
    def test_auto_import(self):
        '''

        '''
        self.bukmarker.auto_import()


    def test_print_rec(self):
        '''
        Print example record without exceptions
        '''
        rec = self.bukmarker.fetch_bm("www.google.com")
        self.bukmarker.print_rec(rec)

    def test_fetch_single_bm(self):
        ''''
        Fetch a non-existent and existing bookmark
        '''

        non_existing_url  = "www.fakegoogle.com"
        rec = self.bukmarker.fetch_bm(non_existing_url)
        self.assertIsInstance(rec,type(None))


#temporary
if __name__ == "main":

    unittest.main(verbosity=2)

