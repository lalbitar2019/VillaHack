import cognitive_face as CF
import requests
import sys
import configparser
from io import BytesIO
from PIL import Image, ImageDraw
import pyodbc

config = configparser.ConfigParser()
config.read('conf.ini')

KEY = config['Default']['key'] 
CF.Key.set(KEY)

BASE_URL = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/'  
CF.BaseUrl.set(BASE_URL)
squad = {'Valeria': u'7526cf4d-f148-4b97-9579-202135e1cfe5', 'Ashley': u'7b009654-c6dc-49ef-ad63-4eed942e0df6', 'Jessica': u'ddd879d5-3861-4e4b-ab0e-462dfc4e229d', 'Meghan': u'2fb9f46f-ec00-46d6-aa26-e093ecacda6f', 'Stephanie': u'b16a25d2-8fda-46ca-ae5d-022751909029', 'Rachel': u'351a7352-4e92-4077-841d-ddd66359abe3', 'Hadley': u'a091502a-8f5a-47a7-a6d3-ff00204af15c', 'Devyn': u'fe10ad2c-cb67-4db4-a0b8-db9fa15ad9bd', 'Maddie': u'61c4f644-193f-4343-937d-996b3c3694f5', 'Lily': u'a8f0529b-9bba-43c4-bb0f-10a8fe0ca321', 'Katie': u'2d10b89e-50d2-4325-9ec8-727b6d21fc98'}
img_url = sys.argv[1]

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


def Who (faceDictionary):
    faceID = faceDictionary['faceId']
    TopPercent = 50
    Who = 'unknown'
    for name in squad:
        result = CF.face.verify(faceID, person_group_id = 'villa-hack', person_id = squad[name])
        Percent = result['confidence'] * 100
        if Percent > TopPercent:
            TopPercent = Percent
            Who = name
    return Who

cnxn = pyodbc.connect(config['Default']['DB'])
try:
    cursor = cnxn.cursor()
    faces = CF.face.detect(img_url, attributes=['emotion'])
    print(faces)

    #Download the image from the url
    # response = requests.get(img_url)
    img = Image.open(img_url)

    #For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)
    for face in faces:
        draw.rectangle(getRectangle(face), outline='red')
        print getEmotions(face)
        print Who(face)

    #Display the image in the users default image browser.
    img.save(img_url.replace('.jpg', '_2.jpg'), 'JPEG')
finally:
    cnxn.close()
