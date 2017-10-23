
import json

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

    root = json_obj["roots"]




if __name__=="__main__":
    read_json_bookmarks()