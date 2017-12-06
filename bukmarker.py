
import json
import sqlite3
import logging
import os
import platform
import datetime
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


# Bukmarker - cmd bookmarking application - integrates with browser bookmarks in one place.

class BukmarkerDB():

    def __init__(self,dbfile=None):
        if dbfile is None:
            self.dbfile = BukmarkerDB.get_default_dbdir()
        else:
            self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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



