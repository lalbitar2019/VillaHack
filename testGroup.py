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

print CF.person_group.get(personGroupID)
print "test"
print CF.person_group.get_status(personGroupID)

print CF.person_group.lists()