# Playing with code related to the project

<<<<<<< Updated upstream
import os
=======
import os,requests,sqlite3

# open firefox db file

conn = sqlite3.connect("C:\\Users\\Devesh\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\x94qotzr.default-1509035816333\\places.sqlite")
#print(conn)
c = conn.cursor()
c.execute(".databases")
for row in c:
    print(row)
>>>>>>> Stashed changes


x = 0
if x > 0:

    raise Exception()
else:
    print(None)
 #   raise WindowsError("x is  0")



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
