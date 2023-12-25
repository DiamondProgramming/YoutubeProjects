import cv2
import face_recognition
import numpy as np
import os

# CREDITS: DiamondPlayer(SMH), COMPLETED ON 26/7/23
# NOTE: HAVE A FOLDER CALLED 'images' IN THE SAME DIRECTORY WITH ALL THE IMAGES OF THE KNOWN FACES

# START CAPTURING VIDEO FROM WEBCAM
cap = cv2.VideoCapture(0)
print('Encoding Started')

# GET KNOWN FACE ENCODINGS AND NAMES
def GetFaceEncodings(folder):
    folder = str(folder)
    faceDatabase = []
    faceDatabase = os.listdir(folder)
    faceEncodingsKnown = []
    print(faceDatabase)
    for faces in faceDatabase:
        img = face_recognition.load_image_file(f"{folder}/{faces}")
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_rgb_encoding = face_recognition.face_encodings(img_rgb)[0]
        faceEncodingsKnown.append(img_rgb_encoding)
    return faceEncodingsKnown

def GetFaceNames(folder):
    folder = str(folder)
    faceDatabase = []
    faceNameKnown = []
    faceDatabase = os.listdir(folder)
    for name in faceDatabase:
        name = os.path.splitext(name)[0]
        faceNameKnown.append(name)
    return faceNameKnown

face_encodings_known = GetFaceEncodings("images")
face_names_known = GetFaceNames('images')

# INITIALIZATION TO AVOID ISSUES LATER
top, bottom, right, left = 0, 0, 0, 0
name = ""
i = 0
face_locations = []
face_encodings = []
face_names = []
pframe = True


# MAIN LOOP
while True:
    ret, frame = cap.read()
   
    # CHECKING IF WEBCAM IS WORKING
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    else:
        print("Receiving stream...")

    # SCALING DOWN THE STREAM FOR FASTER PROCESSING AND LOCATING THE FACE ON SCREEN AND ENCODING IT
    if pframe:
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        small_frame_rgb = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(small_frame_rgb)
        print(f"here debug {face_locations}")
        face_encodings = face_recognition.face_encodings(small_frame_rgb,face_locations)
        face_names = []

        # COMARING FACE IN VIDEO WITH KNWON FACES
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(face_encodings_known, face_encoding)
            face_distances = face_recognition.face_distance(face_encodings_known, face_encoding)
            best_match_index = np.argmin(face_distances)
            name = "Unknown"
            if matches[best_match_index]:
                name = face_names_known[best_match_index]
            face_names.append(name)

    pframe = not pframe
    print(f'Face locations: {face_locations}')

    # EXTRACTING THE LOCATION AND UPSCALING IT AGAIN
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top *=4
        bottom *=4
        right *=4
        left *=4
        print(f'coords: {top} , {bottom} , {right} , {left}')

    # DRAWING THE RECTANGLE AROUND THE FACE AND THE NAME OF THE FACE
    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
    cv2.putText(frame, str(name), (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0,0,255), 1)
    cv2.imshow("Stream", frame)
    key = cv2.waitKey(1)

    # THE 'esc' KEY TO END THE PROGRAM
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
