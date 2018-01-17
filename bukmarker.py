
import json
import sqlite3
import logging
import os
import platform
import datetime
from urllib.request import urlopen
from urllib.error import HTTPError,URLError

import re
from bs4 import BeautifulSoup
from heapq import merge

# logging setup
logger = logging.getLogger("bukmarker.py")
logger.setLevel(logging.DEBUG)

filh = logging.FileHandler("bukmarker.log")
filh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(funcName)s -  %(message)s")
filh.setFormatter(formatter)
logger.addHandler(filh)

__version__ = '0.0.1'
__name__ = 'Devesh Sawant @dsaw'

def merge_no_dupes(*iterables):
    """
    Merge sorted iterables into one unique iterable
    :param *iterables
    :return: merged iterable as a generator
    """

    last = object()

    for val in merge(*iterables):
        if val != last:
            last = val
            yield val
# https://codereview.stackexchange.com/questions/108171/merge-two-list-and-discarding-duplicates


# Bukmarker - cmd bookmarking application - integrates with browser bookmarks in one place.

class BukmarkerDB():

    def __init__(self,dbfile=None):
        if dbfile is None:
            self.dbfile = BukmarkerDB.get_default_dbdir()
        else:
            self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()


    @staticmethod
    def get_default_dbdir():
        '''
            if system is Windows, returns %APPDATA%
            else returns $HOME, if it exists
            else returns current directory

        :return:
         str : path to database file
        '''

        dbfile = os.environ.get("HOME")
        if dbfile is None:
            if platform.system() == "Windows":
                dbfile = os.environ.get("APPDATA")
            else:
                dbfile = os.path.abspath(".")

        dbfile = os.path.join(dbfile,"bukmarker.sqlite")
        return dbfile

    def create_bookmark_db(self):
        """
        Creates bookmark table in cursor if not done yet.
        only run first time
        :return:
        """
        try:
            self.conn = sqlite3.connect(self.dbfile, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            self.cursor = self.conn.cursor()

            self.cursor.execute("""create table  IF NOT EXISTS bookmarks (
                                url text PRIMARY KEY,
                                title text NOT NULL,
                                tags text,
                                description text,
                                last_modified timestamp
             );""")
        except sqlite3.OperationalError as e:
            logger.error(" {} ".format(e))      ## customise error
            raise

    def get_bm_id(self,url):
        """
        Checks if the bookmark exists in the table
        :param url: string of url
        :return: url if it exists,
                -1 if not
        """
        if url is None:
            logger.error("url is blank")
            return -1

        try:
            self.cursor.execute("SELECT * FROM bookmarks WHERE url = ? LIMIT 1;",(url,))
            row = self.cursor.fetchone()

        except Exception as e:
            logger.exception("{}".format(e))
            return -1

        if row is None:
            return -1
        else:
            return url

    # TODO: option to replace existing bookmark
    def add_bookmark_db(self,url,title="", tags="", description="", delay_commit=False):
        """"
        Inserts a bookmark entry in bookmark table
        :param url : url to add
        :param title
        :param tags
        :param description
        :return: -1 if unsuccessful
        """
        # to add error checking

        if url is None:
            logger.error("url is blank")
            return -1

        if self.get_bm_id(url) == url:
            logger.debug("url already exists")
            return -1

        nowtime = datetime.datetime.now()
        self.cursor.execute("""
            INSERT INTO bookmarks VALUES
              (
                ?,
                ?,
                ?,
                ?,
                ?
              );
        """,(url,title,tags,description,nowtime))

        if not delay_commit:
            self.conn.commit()

    def delete_bookmark_db(self,url):
        """
        Deletes bookmark in table with given url
        :param url: bookmark with url to delete
        :return: url if successful
            -1 if unsuccessful
        """
        if url is None:
            logger.error("url is blank")
            return -1

        query = "DELETE FROM bookmarks WHERE url = ?"
        try:
            self.cursor.execute(query,(url,))
            if self.cursor.rowcount == 1:
                print("Deleted {} successfully".format(url))
                self.conn.commit()
                return url
            else:
                print("Bookmark with {} doesn't exist".format(url))
                logger.debug("bookmark with {} doesn't exist".format(url))
                return -1
        except Exception as e:
            logger.exception("{}".format(e))
            return -1

    def modify_bookmark_db(self,url,title=None, tags_in=None, description=None):
        """
        Updates bookmark column in table with  given attributes.
        Will automatically fetch url from table (todo)

        :param title:
        :param tags_in: string
                tags should be comma separated in the string
        :param description:
        :return: -1 if unsuccessful
        """

        query = "UPDATE bookmarks SET "
        params = ()
        to_update = False

        if url is None:
            # TODO automatically fetch url
            logger.error("url is blank")
            return -1

        if title is not None:
            query += "title = ?, "
            params += (title,)
            to_update = True

        if tags_in is not None:
            # TODO handle various input string anomalies
            tags_in = tags_in.strip(", ")

            query += "tags = ?, "
            params += (tags_in,)
            to_update = True

        if description is not None:
            query += "description = ?, "
            params += (description,)
            to_update = True

        if not to_update:
            title = self.fetch_title_bookmark("https://" + url)
            if title == -1:
                print("Unable to fetch title...")
                return -1
            query += "title = ?, "
            params += (title,)
            to_update = True
        nowtime = datetime.datetime.now()

        params += (nowtime,url)
        query = query.strip(" ")
        query += " last_modified = ?  WHERE url = ?;"

        try:
            self.cursor.execute(query,params)
            if self.cursor.rowcount == 1:
                print("Updated {} successfully".format(url))
                self.conn.commit()
                return url
            else:
                print("Bookmark with {} doesn't exist".format(url))
                logger.debug("bookmark with {} doesn't exist".format(url))
                return -1
        except Exception as e:
            logger.exception("{}".format(e))
            return -1

    def append_tags(self,url,tag_set):
        """
        Appends new tags passed in to bookmark record.
        :param url:
        :param tag_set:
        :return: -1 if unsuccessful
        """
        if url is None:
            logger.error("url is blank")
            return -1

        self.cursor.execute("SELECT url,tags from bookmarks where url = ?", (url,))
        results = self.cursor.fetchone()
        if results:
            old_tags = results[1]
            old_tags = old_tags.split(',')
            old_tags = sorted(old_tags)
            tag_set = sorted(tag_set)
            final_tags = merge_no_dupes(tag_set,old_tags)
            final_tags_str = ','.join(final_tags)
            logger.debug(final_tags_str)
            query = "UPDATE bookmarks SET tags = ?,last_modified = ? WHERE url = ?"

            self.cursor.execute(query,(final_tags_str,datetime.datetime.now(),url))
            if self.cursor.rowcount == 1:
                logger.debug("bookmark updated")
                self.conn.commit()
        else:
            logger.error("No such bookmark exists")
            return -1

        return url

    def delete_tags(self,url,tags):
        """
        Deletes specified tags of given url
        :param url:
        :param tags: Comma-separated string
        :return: -1 if unsuccessful
        """
        tag_set = tags.strip("\n ").split(",")
        if url is None:
            logger.error("url is blank")
            return -1

        self.cursor.execute("SELECT url,tags from bookmarks where url = ?", (url,))
        results = self.cursor.fetchone()
        if results:
            fetched_tags = results[1].strip(" ,")
            for tag in tag_set:
                if fetched_tags.find(tag) == 0:
                    fetched_tags = fetched_tags.replace(tag + ",","",1)
                else:
                    fetched_tags = fetched_tags.replace("," + tag,"",1)

            query = "UPDATE bookmarks SET tags = ?, last_modified  = ? WHERE url = ?"
            nowtime = datetime.datetime.now()
            self.cursor.execute(query, (fetched_tags,nowtime, url))
            if self.cursor.rowcount == 1:
                logger.debug("bookmark with tags {0} deleted".format(fetched_tags))
                self.conn.commit()
        else:
            logger.error("No bookmark returned to delete tags from")
            return -1

        return url

    def search_by_url(self,url):
        """
        Searches record by url and returns record
        :param url:
        :return: tuple of bookmark
        """
        if url is None:
            logger.error("url is blank")
            return -1

        query = "SELECT * FROM bookmarks WHERE url = ? "
        self.cursor.execute(query,(url,))
        results = self.cursor.fetchone()
        if results:
            logger.debug(tuple(results))
            return results
        return -1

    def parse_tags(self,keywords=[]):
        """
        Parse list of keywords and returns delimited list
        :param keywords: list, optional
            List of tags to parse
        :return: None, if keywords is None
            ',', if keywords is an empty list

        """

        if keywords is None:
            return None

        if not keywords:
            return ','

        tagstr = ','.join(keywords)

        marker = tagstr.find(",")
        finallist = []
        while marker != -1:
            finallist.append(tagstr[:marker].strip())
            tagstr = tagstr[marker+1:]
            marker = tagstr.find(",")

        finalstr = ','.join(sorted(set(finallist)))
        return finalstr

    def prep_tags(self, tagstr):
        """"
        Processes tag string and returns list of tags and type of search operator
        :param tagstr: str
        :return: (taglist,searchop)
        """
        if '+' in tagstr and ',' in tagstr:
            logger.error("Both and & are not allowed")
            return -1

        if '+' in tagstr:
            taglist = tagstr.split('+')
            searchop = '+'
        else:
            taglist = tagstr.split(',')
            searchop = '|'

        # clean list of tags
        taglist = list(map( lambda s : s.strip(), taglist))

        return (taglist,searchop)

    def search_by_tags(self,tags):
        """
        Searches record by tags
        Uses regex
        :param tags: string separated by either | or +
        :return: list of results
        """

        (taglist,searchop) = self.prep_tags(tags)

        search_query = r''
        def regexp(y,x,search = re.search):
            return 1 if search(y,x) else 0
        self.conn.create_function('regexp',2,regexp)

        if searchop == '+':
            wrappedtags = map( lambda s : r'(?=.*' + s + r')', taglist)
            search_query = r''.join(wrappedtags)
        else:
            wrappedtags = map( lambda s: r'(?=' + s + r')',taglist)
            search_query = r'|'.join(wrappedtags)

        res = self.cursor.execute('SELECT url,title FROM bookmarks WHERE tags REGEXP ?', (search_query,))
        return res.fetchall()

    def print_rec(self,row):
        """
        Prints bookmark record for display
        :param row: Sqlite3 row object
        :return:
        """

        print("url {0:30}".format(row["url"]))
        print("- {0}".format(row["title"]))
        print("> {}".format(row["tags"]))
        print("+ {}".format(row["description"]))



    def fetch_title_bookmark(self,url):
        """
        Opens web page at url and fetches the title
        :param url: if empty logs error
        :return: title or -1 if url empty
        """

        if url is None:
            logger.error("url is blank")
            return -1

        try:
            bm_req = urlopen(url)
        except HTTPError as e:
            logger.error(" {}, {} ".format(e.code,e.reason[1]))
            return -1
        except URLError as e:
            logger.error("{}, {}".format(*e.reason))
            return -1
        else:
            bm_soup = BeautifulSoup(bm_req,"lxml")
            return bm_soup.title.string

    def read_firefox_bookmarks_db(self, dbfile="C:\\Users\\Devesh\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\x94qotzr.default-1509035816333\\places.sqlite"):
        """
        Reads bookmark places.sqlite file and stores it as a bookmark dictionary
        :param dbfile:
        :return: dict: key is url, value is another dict
        """

        conn = sqlite3.connect(dbfile)
        # print(conn)
        c = conn.cursor()
        # parent folder rows
        # foreign key is null for folders
        folder_bm = {}
        c.execute("SELECT DISTINCT id,title FROM 'moz_bookmarks' WHERE type=2")
        for row in c.fetchall():
            folder_bm[row[0]] = row[1]
        # print(folder_bm)

        c.execute("SELECT DISTINCT fk,parent,title FROM 'moz_bookmarks' WHERE type=1")
        # loaded bookmark dict
        bm = {}

        for row in c.fetchall():
            res = c.execute("SELECT url FROM 'moz_places' where id={}".format(row[0]))
            res = res.fetchone()
            bm[res[0]] = {"title": row[2], "tags": [folder_bm[row[1]]]}   # parent folder title as tag

        print(bm)
        return bm

    def read_json_bookmarks(self, filename="C:\\Users\Devesh\AppData\Local\Google\Chrome\\User Data\Default\Bookmarks"):

        with open(filename) as f:
            bm_json = json.load(f)

        return bm_json

    def load_chrome_bookmarks(self, json_obj):
        """
         Gets bookmarks from json object
        :param json_obj:
        :return:
        """
        data = json_obj["roots"]
        return data

    def get_folder_bookmark_list(self, json_folder):
        """ Extracts children list from boookmark folder object

        -----
        :param json_folder : dict
            Dictionary object which is boookmark folder

        :return:
        -----
        list
            list of children dictionaries
        None
            if not folder object
        """

        if json_folder is None:
            return None

        if json_folder["type"] != "folder":
            raise Exception(" json_folder not a bookmark folder")
        # ignores folders
        child_bookmark_list = [elem for elem in json_folder["children"] if elem["type"] == "url"]
        print(child_bookmark_list)
        return child_bookmark_list

    # recursive - need to test!
    def traverse_bm_folder(self, child_sublist, parent_folder):
        """
        Generator function
        :param child_sublist: list
        :param parent_folder: str
        :return:
        """

        if not isinstance(child_sublist, list):
            raise Exception(" Child_sublist not a list")
        # recursive yield of url
        for item in child_sublist:
            if item['type'] == 'folder':
                self.traverse_bm_folder(item['children'], item['name'])
                logger.debug("Folder traversed : {0}".format(item['name']))
            elif item['type'] == 'url':
                yield item


if __name__ == "__main__":
    #chrome_bm = load_chrome_bookmarks(read_json_bookmarks())
    pass
    # iterate over json
    # for bkey,bval in chrome_bm.items():

    #    if chrome_bm[bkey]["type"] == "folder":
    #         print("Bookmark Folder - {0}".format(bkey))
    #        for bm in get_folder_bookmark_list(bval):
    #           print("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))

    # test traverse function



