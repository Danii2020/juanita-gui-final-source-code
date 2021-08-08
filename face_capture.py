import cv2
import os
import imutils

person = 'Daniel'
data_path = 'Data_Face'
person_path = data_path + '/' + person

if not os.path.exists(person_path):
    os.makedirs(person_path)

capture = cv2.VideoCapture('Video_Daniel.mp4')

face_classif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count = 0

while True:
    comp, frame = capture.read()
    if comp == False: break
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aux_frame = frame.copy()

    faces = face_classif.detectMultiScale(gray, 1.3, 7)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        face = aux_frame[y:y+h, x:x+w]
        face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(person_path + f'/face_{count}.jpg', face)
        count += 1
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27 or count >= 300:
        break

capture.release()
cv2.destroyAllWindows()