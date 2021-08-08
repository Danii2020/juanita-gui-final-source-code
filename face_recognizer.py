import cv2
import os
import threading as tr
import subprocess as sub
import winsound

data_path = 'C:\\Users\\PC\\Desktop\\Python\\Juanita AI\\Experimentos\\Data_Face'
image_paths = os.listdir(data_path)
# print('image_paths=', image_paths)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# Leyendo el modelo
face_recognizer.read('C:\\Users\\PC\\Desktop\\Python\\Juanita AI\\Experimentos\\LBPHFaceModel.xml')


face_classif = cv2.CascadeClassifier('C:\\Users\\PC\\Desktop\\Python\\Juanita AI\\Experimentos\\haarcascade_frontalface_default.xml')

def face_rec(state):
    capture = cv2.VideoCapture(0)
    while True:
        comp, frame = capture.read()
        if comp == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = gray.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = aux_frame[y:y+h, x:x+w]
            face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(face)
        
            cv2.putText(frame, f'{result}', (x, y-5), 1, 1.3, (255,255,0), 1, cv2.LINE_AA)

            # LBPHFace
            if result[1] < 76:
         
                cv2.putText(frame, f'{image_paths[result[0]]}', (x, y-25), 2, 1.1, (0,255,0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)                              
            else:
                thread_alarma_song(0)        
                cv2.putText(frame, 'Desconocido', (x, y-20), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)  
                        
                



        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & state == 1:
            sub.call(f'taskkill /IM python.exe /F', shell=True)            
            break            
            cap.release()
            cv2.destroyAllWindows()
            
            

def alarma_song(state):    
    if state == 0:
        winsound.PlaySound("alarmaa.wav", winsound.SND_FILENAME)
def thread_alarma_song(state):    
    ta = tr.Thread(target=alarma_song, args=(state,))
    ta.start()
