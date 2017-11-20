
import json
import sqlite3
import logging,os,platform
# logging setup
logging.basicConfig(filename='bukmarker.log',level=logging.DEBUG)

__version__ = '0.0.1'
__name__ = 'Devesh Sawant @dsaw'


# Bukmarker - cmd bookmarking application - integrates with browser bookmarks in one place.

class BukmarkerDB():

    def __init__(self,conn,cursor,dbfile=None):
        self.conn = conn
        self.cursor = cursor
        self.dbfile = dbfile

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

        dbfile = os.path.join(dbfile,"buku")
        return dbfile

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
            raise Exception(" child_sublist not a list")
        # recursive yield of url
        for item in child_sublist:
            if item['type'] == 'folder':
                self.traverse_bm_folder(item['children'], item['name'])
                logging.debug("Folder traversed : {0}".format(item['name']))
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



