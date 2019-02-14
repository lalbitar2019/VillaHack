import cognitive_face as CF
import requests
import sys
import configparser
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageDraw
import pyodbc

config = configparser.ConfigParser()
config.read('conf.ini')

KEY = config['Default']['key'] 
CF.Key.set(KEY)

BASE_URL = 'https://centralus.api.cognitive.microsoft.com/face/v1.0/'  
CF.BaseUrl.set(BASE_URL)
squad = {'Valeria': u'3b8d1352-a40f-4d3b-b961-b71a1b6df573', 'Ashley': u'd5607412-789f-41f5-b1a5-a9818f21f638', 'Jessica': u'148e2c70-4d81-40b7-bf9e-843b3828e57a', 'Meghan': u'94cc2454-fa5c-4492-8961-69509d52dc9b', 'Stephanie': u'792184cb-6cb6-45e6-a311-3e30e223d478', 'Rachel': u'56c42b10-9ff1-497f-b115-d581296eefbe', 'Hadley': u'44761499-f06e-47a0-90f7-320332d63c3a', 'Devyn': u'5d094402-9d63-465f-a19d-59d8c55e35c3', 'Maddie': u'95d137be-01a0-4990-8da4-5926ed518956', 'Lily': u'53bebb64-0e6e-4626-bea0-b1f636f3ddf8', 'Katie': u'bbd75b8c-2801-44a5-a7fd-a395c2d66b70'}
img_url = sys.argv[1]

def drawrect(drawcontext, xy, outline=None, width=0):
    (x1, y1), (x2, y2) = xy
    points = (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
    drawcontext.line(points, fill=outline, width=width)

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
    returnDict = {'topemotion':None,'toppercent':0,'validemotions':{}}

    for emotion in emotions:
        percent = emotions[emotion] * 100
        if percent > 10:
            returnDict['validemotions'][emotion] = percent
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

# conn = pyodbc.connect(config['Default']['DB'])
try:
    # cursor = conn.cursor()
    # cursor.execute("insert into images(image_path, status) values ('"+img_url+"', 'PROCESSING')")
    # conn.commit()
    faces = CF.face.detect(img_url, attributes=['emotion'])
    print(faces)

    #Download the image from the url
    # response = requests.get(img_url)
    img = Image.open(img_url)

    #For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Aaargh.ttf", 150)
    for face in faces:
        rec = getRectangle(face)
        drawrect(draw, rec, outline='red', width=5)
        # draw.rectangle(getRectangle(face), outline='red')
        emotions = getEmotions(face)
        print emotions
        who = Who(face)
        draw.text( (rec[0][0], rec[0][1]) ,who,(255,255,255),font=font)
        yShift = 0
        for emotion in emotions['validemotions']:
            print emotion
            draw.text( ((rec[0][0] + rec[1][0])/2, (rec[0][1] + yShift)) ,emotion,(255,255,255),font=font)
            yShift = yShift + 150
            analysisSQL = "INSERT INTO IMAGE_ANALYSIS(STUDENT_ID, EMOTION, PERCENTAGE, IMAGE_ID) values ((select ID FROM STUDENTS WHERE face_id = '"+squad[who]+"'), '"+emotion+"', "+str(int(emotions['validemotions'][emotion]))+", (select ID FROM IMAGES WHERE IMAGE_PATH = '"+img_url+"'))"
            # print analysisSQL
            # cursor.execute(analysisSQL)

    #Display the image in the users default image browser.
    img.save(img_url.replace('.jpg', config['Default']['Replace']), 'JPEG')
    # cursor.execute("update images set status = 'SUCCESS' where image_path = '"+img_url+"'")
    # conn.commit()
except Exception as e:
    # cursor.execute("update images set status = 'FAIL' where image_path = '"+img_url+"'")
    # conn.commit()
    raise e
finally:
    # conn.close()
    pass
