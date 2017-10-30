
import json
import sqlite3
import logging


__version__ = '0.0.1'
__name__ = 'Devesh Sawant @dsaw'



# logging setup
logging.basicConfig(filename='bukmarker.log',level=logging.DEBUG)
logger = logging.getLogger()

# Bukmarker - cmd bookmarking application - integrates with browser bookmarks in one place.


# filename parameter is Chrome bookmarks file in Windows

def read_json_bookmarks(filename="C:\\Users\Devesh\AppData\Local\Google\Chrome\\User Data\Default\Bookmarks"):

    with open(filename) as f:
        bm_json = json.load(f)

    return bm_json


def load_chrome_bookmarks(json_obj):
    """
     Gets bookmarks from json object
    :param json_obj:
    :return:
    """

    data = json_obj["roots"]
    return data


def get_folder_bookmark_list(json_folder):
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

def traverse_bm_folder(child_sublist, parent_folder):
    """
    Generator function
    :param child_sublist: list
    :param parent_folder: str
    :return:
    """
    if not isinstance(child_sublist,list):
        raise Exception(" child_sublist not a list")
    # recursive yield of url
    for item in child_sublist:
        if item['type'] == 'folder':
            traverse_bm_folder(item['children'], item['name'])
            logging.debug("Folder traversed : {0}".format(item['name']))
        elif item['type'] == 'url':
            yield item


if __name__ == "__main__":
    chrome_bm = load_chrome_bookmarks(read_json_bookmarks())

    # iterate over json
    # for bkey,bval in chrome_bm.items():

    #    if chrome_bm[bkey]["type"] == "folder":
    #         print("Bookmark Folder - {0}".format(bkey))
    #        for bm in get_folder_bookmark_list(bval):
    #           print("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))

    # test traverse function

    for bkey,bval in chrome_bm.items():

        if bval["type"] == "folder":
            print("Bookmark Folder - {0}".format(bkey))

            for bm in traverse_bm_folder(bval["children"], bval["name"]):
                print("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))

