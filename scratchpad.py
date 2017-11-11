# Playing with code related to the project

#<<<<<<< Updated upstream
#import os
import os,requests,sqlite3,logging

logging.basicConfig(filename='bukmarker.log', level=logging.DEBUG)
# open firefox db file

conn = sqlite3.connect("C:\\Users\\Devesh\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\x94qotzr.default-1509035816333\\places.sqlite", \
                       detect_types=sqlite3.PARSE_COLNAMES|sqlite3.PARSE_DECLTYPES)
conn.row_factory = sqlite3.Row
#print(conn)
c = conn.cursor()

# parent folder rows
# foreign key is null for folders
folder_bm = {}
c.execute("SELECT DISTINCT id,title FROM 'moz_bookmarks' WHERE type=2")
for row in c.fetchall():
    folder_bm[row[0]] = row[1]
#print(folder_bm)

c.execute("SELECT DISTINCT fk,parent,title,dateAdded FROM 'moz_bookmarks' WHERE type=1")
# loaded bookmark dict
bm = {}


for row in c.fetchall():
    res = c.execute("SELECT url FROM 'moz_places' where id={}".format(row[0]))
    res = res.fetchone()
    bm[res[0]] = { "title":row[2], "tags":[folder_bm[row[1]]], "date_added":row[3] }
    logging.debug(" {0} ".format(row["dateAdded"]))

#print(bm)
# fetch date_added from db






#>>>>>>> Stashed changes





print(os.getcwd())
env = os.environ

print(env.get('APPDATA'))


print(os.path.join(env.get('APPDATA'),'dev'))

def f():
    yield 3
    yield 5
    raise StopIteration



def h():
    g = []
    g.extend(f())
    print(g)
    print(len(g))

h()
