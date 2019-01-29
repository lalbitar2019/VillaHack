import cognitive_face as CF
import requests
import sys
import configparser
from io import BytesIO
from PIL import Image, ImageDraw


config = configparser.ConfigParser()
config.read('conf.ini')

KEY = config['Default']['key'] 
CF.Key.set(KEY)

BASE_URL = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/'  
CF.BaseUrl.set(BASE_URL)

img_url = sys.argv[1]
faces = CF.face.detect(img_url, attributes=['emotion'])
print(faces)

#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


def getEmotions(faceDictionary):
    emotions = faceDictionary['faceAttributes']['emotion']
    returnDict = {'topemotion':None,'toppercent':0,'validemotions':[]}

    for emotion in emotions:
        percent = emotions[emotion] * 100
        if percent > 10:
            returnDict['validemotions'].append({emotion:percent})
            if percent > returnDict['toppercent']:
                returnDict['topemotion'] = emotion
                returnDict['toppercent'] = percent

    return returnDict
    
    
    

#Download the image from the url
# response = requests.get(img_url)
img = Image.open(img_url)

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')
    print getEmotions(face)

#Display the image in the users default image browser.
img.save(img_url.replace('.jpg', '_2.jpg'), 'JPEG')
