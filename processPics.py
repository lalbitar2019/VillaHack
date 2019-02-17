import os

directory = 'pictures'

for filename in os.listdir(directory):
    cmd = 'python FaceQuickstart.py '+ directory + '\\' + filename
    print cmd
    os.system(cmd)
