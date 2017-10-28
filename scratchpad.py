

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
