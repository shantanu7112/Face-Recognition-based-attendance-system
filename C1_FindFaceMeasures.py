import cv2
import math
import os
import copy

path = "dataset/"

folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

# Load the face detector
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('detector_architectures/haarcascade_smile.xml')

strVal = ''
outCount = 1

for pathCount in range (0, len(folders)) :
    folder = path + "/" + folders[pathCount] + "/"
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    for fileCount in range(0, len(files)) :
        # Read the image
        filePath = folder + files[fileCount]
        image = cv2.imread(filePath)
        
        # Detect faces in the image
        faces = face_detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # For each face in the image
        for face in faces:
        
            # Extract the face region
            face_region = image[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
            face_region = cv2.resize(face_region, (256, 256))
            face_region_bkp = copy.copy(face_region)
            
            # Extract the eyes, nose, and mouth from the face region
            eyes = []
            nose = []
            mouth = []
            
            eyes = eye_cascade.detectMultiScale(face_region)
            nose = nose_cascade.detectMultiScale(face_region)
            mouth = mouth_cascade.detectMultiScale(face_region)
            
            if(len(eyes) == 0) :
                continue
            
            eye = eyes[0]
            cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0]+eye[2], eye[1]+eye[3]), (255, 0, 0), 2)
            if(len(eyes) > 1) :
                eye = eyes[1]
                points = [eyes[0], eyes[1]]
            else :
                eye = eyes[0]
                points = [eyes[0], eyes[0]]
            

            cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0]+eye[2], eye[1]+eye[3]), (255, 0, 0), 2)
            for count in range(0, len(nose)) :
                n = nose[count]
                if(n[1]  > eye[1]) :
                    eye = n
                    points.append(eye)
                    cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0]+eye[2], eye[1]+eye[3]), (255, 0, 0), 2)
                    break
                
            for count in range(0, len(mouth)) :
                n = mouth[count]
                if(n[1]  > eye[1]) :
                    eye = n
                    points.append(eye)
                    cv2.rectangle(face_region, (eye[0], eye[1]), (eye[0]+eye[2], eye[1]+eye[3]), (255, 0, 0), 2)
                    break
            eye = eyes[0]
            fname = 'faces/%d.bmp'%(outCount)
            face_region_bkp[:, :, 0] = outCount-1
            cv2.imwrite(fname, face_region_bkp, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            outCount = outCount + 1
            
            dists = []
            for count in range(0, len(points)) :
                p1 = points[count]
                x1 = p1[0] + p1[2]/2
                y1 = p1[1] + p1[3]/2
                
                for count2 in range(0, len(points)) :
                    p2 = points[count]
                    x2 = p2[0] + p2[2]/2
                    y2 = p2[1] + p2[3]/2
                    dist = math.sqrt( math.pow(x1-x2, 2) + math.pow(y1-y2, 2) )

                    dists.append(dist)
            print(dists)
            
            
            for count in range(0, len(dists)) :
                strVal = strVal + str(dists[count]) + ","
            strVal = strVal + folders[pathCount] + "\n"
            
            # Display the face region
            cv2.imshow("Face", face_region)
            cv2.waitKey(100)
        cv2.destroyAllWindows()

f = open('datasets.csv', 'w')
f.write(strVal)
f.close()