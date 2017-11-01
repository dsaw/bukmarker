# Playing with code related to the project

import os


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
