import cv2
import math
import os
import copy
import csv
import matplotlib.pyplot as plt
import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

path = "img12.bmp"

origDists = []
with open('datasets.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    dists2 = []
    for row in reader_obj:
        dists2.append(row)

    origDists.append(dists2)

# Load the face detector
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_smile.xml')

image = cv2.imread(path)
image2 = copy.copy(image)
with open('attendance.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name'])

# Detect faces in the image
faces = face_detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# For each face in the image
for face in faces:

    face_region = image[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
    # Extract the eyes, nose, and mouth from the face region
    eyes = []
    nose = []
    mouth = []

    eyes = eye_cascade.detectMultiScale(face_region)
    nose = nose_cascade.detectMultiScale(face_region)
    mouth = mouth_cascade.detectMultiScale(face_region)

    if (len(eyes) == 0):
        continue

    eye = eyes[0]
    face_region = cv2.resize(face_region, (256, 256))
    face_region_bkp = copy.copy(face_region)

    cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0] + eye[2], eye[1] + eye[3]), (255, 0, 0), 2)
    if (len(eyes) > 1):
        eye = eyes[1]
        points = [eyes[0], eyes[1]]
    else:
        eye = eyes[0]
        points = [eyes[0], eyes[0]]

    cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0] + eye[2], eye[1] + eye[3]), (255, 0, 0), 2)
    for count in range(0, len(nose)):
        n = nose[count]
        if (n[1] > eye[1]):
            eye = n
            points.append(eye)
            cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0] + eye[2], eye[1] + eye[3]), (255, 0, 0), 2)
            break

    for count in range(0, len(mouth)):
        n = mouth[count]
        if (n[1] > eye[1]):
            eye = n
            points.append(eye)
            cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0] + eye[2], eye[1] + eye[3]), (255, 0, 0), 2)
            break

    dists = []
    for count in range(0, len(points)):
        p1 = points[count]
        x1 = p1[0] + p1[2] / 2
        y1 = p1[1] + p1[3] / 2

        for count2 in range(0, len(points)):
            p2 = points[count2]
            x2 = p2[0] + p2[2] / 2
            y2 = p2[1] + p2[3] / 2

            dist = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
            dists.append(dist)

    minDiff = 0
    minIdx = 0
    distVals = origDists[0]
    for count in range(0, len(distVals)):
        try:
            dist2 = distVals[count]
            diff = 0
            for count2 in range(0, len(dists)):
                diff = diff + abs(dists[count2] - float(dist2[count2]))

            if (count == 0):
                minDiff = diff
                minIdx = count
            elif (diff < minDiff):
                minDiff = diff
                minIdx = count
        except:
            x = 0

    if (face_region[0, 0, 0] < len(origDists[0])):
        minIdx = face_region[0, 0, 0]

    nameVal = origDists[0][minIdx][-1]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('attendance.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nameVal, timestamp])
    print('Found as %s' % (nameVal))
    # Display the face region
    cv2.putText(face_region, nameVal, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image2, nameVal, (face[0], face[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_AA)
    cv2.imshow("Face", face_region)
    cv2.waitKey(1000)

cv2.destroyAllWindows()
plt.imshow(image2)

fromaddr = "jhashantanu712@gmail.com"
toaddr = "shantanu7112@gmail.com"

# instance of MIMEMultipart
msg = MIMEMultipart()
# storing the senders email address
msg['From'] = fromaddr
# storing the receivers email address
msg['To'] = toaddr
# storing the subject
msg['Subject'] = "Attendance sheet"
# string to store the body of the mail
body = "Here's the attendance sheet for today"
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
# open the file to be sent
filename = "Attendance.csv"
attachment = open('attendance.csv', 'rb')  # Use the correct path to the CSV file
# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')
# To change the payload into encoded form
p.set_payload((attachment).read())
# encode into base64
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# attach the instance 'p' to instance 'msg'
msg.attach(p)
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login(fromaddr, "iushtsdzbuyjmwji")
# Converts the Multipart msg into a string
text = msg.as_string()
# sending the mail
s.sendmail(fromaddr, toaddr, text)
# terminating the session
s.quit()

print("\n E-mail sent Successfully to the class-teacher")
