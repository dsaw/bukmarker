
import json
import sqlite3

__version__ = '0.0.1'
__name__ = 'Devesh Sawant @dsaw'


## Bukmarker - cmd bookmarking application - integrates with browser bookmarks in one place.


## filename parameter is Chrome bookmarks file in Windows

def read_json_bookmarks(filename="C:\\Users\Devesh\AppData\Local\Google\Chrome\\User Data\Default\Bookmarks"):


    with open(filename) as f:
        bm_json = json.load(f)

    return bm_json


def load_chrome_bookmarks(json_obj):
    '''
     Gets bookmarks from json object
    :param json_obj:
    :return:
    '''

    data = json_obj["roots"]
    return data


def get_folder_bookmark_list(json_folder):
    '''


    '''

    if json_folder["type"] != "folder":
        raise Exception(" Json object not of type folder")
    # ignores folders
    child_bookmark_list = [elem for elem in json_folder["children"] if elem["type"] == "url"]
    print(child_bookmark_list)
    return child_bookmark_list







if __name__=="__main__":
    chrome_bm = load_chrome_bookmarks(read_json_bookmarks())

    # iterate over json
    for bkey,bval in chrome_bm.items():

        if chrome_bm[bkey]["type"] == "folder":
            print("Bookmark Folder - {0}".format(bkey))
            for bm in get_folder_bookmark_list(bval):
                print("{name} : {url} ".format(name=bm.get("name"), url=bm.get("url")))


