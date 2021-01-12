import glob
import face_recognition
import cv2
import numpy as np
import os
from keras.models import load_model
from keras.utils import get_file



# Once download of Gender Weights
#dwnld_link = "https://s3.ap-south-1.amazonaws.com/arunponnusamy/pre-trained-weights/gender_detection.model"
#model_path = get_file("gender_detection.model", dwnld_link,
#                      cache_subdir="pre-trained", cache_dir=os.getcwd())

#fmodel = load_model(model_path)
#classes = ['woman', 'man']       # gender classes


def image_to_embedding(image, model):  # Converts image into embed for InceptionNet

    image = cv2.resize(image, (96, 96))
    img = image[..., ::-1]
    img = np.around(np.transpose(img, (0, 1, 2))/255.0, decimals=12)
    x_train = np.array([img])
    embedding = model.predict_on_batch(x_train)
    return embedding


def create_input_image_embeddings():  # Creates input embedding for all images in images directory
    i = 0
    for file in glob.glob("FaceRecognition/images/*"):
        person_name = os.path.splitext(os.path.basename(file))[0]
        image_file = cv2.imread(file, 1)
        #input_embeddings[person_name] = image_to_embedding(image_file, model)
        image = face_recognition.load_image_file(file)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        known_face_names.append(person_name)
        i = i+1
    #print("no of registered users ", i)


def recognize_face(face_image, input_embeddings, model):  # Finidng Eucledian distance using Inception Model

    embedding = image_to_embedding(face_image, model)

    minimum_distance = 200
    name = None

    # Loop over  names and encodings.
    for (input_name, input_embedding) in input_embeddings.items():

        euclidean_distance = np.linalg.norm(embedding-input_embedding)

        #print('Euclidean distance from %s is %s' %(input_name, euclidean_distance))

        if euclidean_distance < minimum_distance:
            minimum_distance = euclidean_distance
            name = input_name

    if minimum_distance < 0.68:
        return str(name)
    else:
        return None


def imgasave(img, name):  # Function to save image
    path = "FaceRecognition/images/"+name+".jpg"
    cv2.imwrite(path, img)


def imgasave2(img, name):  # Function to save image
    path = "FaceRecognition/fullimage/"+name+".jpg"
    cv2.imwrite(path, img)




known_face_encodings = []
known_face_names = []

input_embeddings = {}

updateinreg = False


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
speakfacenames = []

speakreg = False
Unknowniteration = 0
knowniteration = 0
speakhi = False
face_names = []
updateinreg = True
oldname = []
create_input_image_embeddings()  # Create embedding for all present images
# print(known_face_names)
def FaceRceco(frame, updateinreg=False,knowniteration = 0):
    
    #ret, frame = video_capture.read()
    if updateinreg:  # If there is update inregistered users then update embeddings
        known_face_names.clear()
        known_face_encodings.clear()
        create_input_image_embeddings()
        updateinreg = False
    newframe = frame.copy()  # Save a copy of frame for saving perpose
    # Resize frame of video to 1/4 size for faster face recognition processing
    #("SHAPE "+str(frame.shape))
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #print(small_frame.shape)
    #small_frame = frame
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        #print(name)
        face_names.append(name)

    #print(face_locations)
    left = 0
    right = 0
    bottom = 0
    top = 0
    sname = []
    r = cv2.rectangle(frame, (1, 1), (1, 1), (0, 255, 0), 1)  # just diclaration for furtur refeance
    # Display the results

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        #print()
        # Draw a box around the face
        r = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)



        #print (r)
        # Draw a label with a name below the face
        # print("name",name,"old_name",oldname)

        sname.append(name)
        #print(name)
        # print("name",name,"old_name",oldname,"sname",sname)

        cropframe = frame[int(top):int(bottom), int(left):int(right)]
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        #if knowniteration >= 3 or Unknowniteration >= 3:
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        face_names.clear()
        #print("faceDetected")
    #cv2.imshow('Video', frame)
    return frame
'''
video_capture = cv2.VideoCapture(0)  # Capture video from webcam 0

while True:
    ret, frame = video_capture.read()
    frame = FaceRcecognition(frame, updateinreg=False)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

'''
    #cv2.imshow(frame)

