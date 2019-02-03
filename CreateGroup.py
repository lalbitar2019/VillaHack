import cognitive_face as CF
import requests
import sys
import configparser
from io import BytesIO
from PIL import Image, ImageDraw
import os

config = configparser.ConfigParser()
config.read('conf.ini')

KEY = config['Default']['key'] 
CF.Key.set(KEY)

BASE_URL = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/'  
CF.BaseUrl.set(BASE_URL)

personGroupID = 'villa-hack'

try:
    CF.person_group.get(personGroupID)
    CF.person_group.delete(personGroupID)
    print 'deleted old group'
except CF.util.CognitiveFaceException as e:
    print 'no group to delete'

CF.person_group.create(personGroupID)

output = {}
directory = 'pictures\headShots'

for filename in os.listdir(directory):
    person = CF.person.create(personGroupID,filename)
    output[filename] = person['personId']
    print filename
    for imagename in os.listdir(directory + '\\' + filename):
        if imagename[0] != 'A':
            print imagename
            CF.person.add_face(directory + '\\' + filename + '\\' + imagename, personGroupID, person['personId'])
        

CF.person_group.train(personGroupID)
print output
