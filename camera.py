import threading
import binascii
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64
import numpy as np
import cv2
from PIL import Image



from FaceRecognition.facerec import FaceRceco
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

def Process(to_process):
    # input is an ascii string.
    input_str = to_process

    # convert it to a pil image
    input_img = base64_to_pil_image(input_str)

    open_cv_image = np.array(input_img)
    # print("recived")

    open_cv_image = cv2.resize(open_cv_image, (640, 480))
    open_cv_image = FaceRceco(open_cv_image,updateinreg = True)
    open_cv_image = cv2.resize(open_cv_image, (300, 150))
    # cv2.imwrite("image.jpg",open_cv_image)
    img = Image.fromarray(open_cv_image)

    # output_img is an PIL image
    output_img = img

    output_str = pil_image_to_base64(output_img)

    # convert eh base64 string in ascii to base64 string in _bytes_
    # print(output_str)
    to_output = output_str
    return to_output

class Camera(object):
    def __init__(self, makeup_artist):
        self.to_process = ''
        self.to_output = ''
        self.makeup_artist = makeup_artist

        '''thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()'''

    def process_one(self):
        if not self.to_process:
            return

        # input is an ascii string. 
        input_str = self.to_process

        # convert it to a pil image
        input_img = base64_to_pil_image(input_str)

        open_cv_image = np.array(input_img)
        #print("recived")

        open_cv_image = cv2.resize(open_cv_image, (640,480))
        print("Detected")
        open_cv_image = FaceRceco(open_cv_image,updateinreg = True)
        open_cv_image = cv2.resize(open_cv_image, (300, 150))
        #cv2.imwrite("image.jpg",open_cv_image)
        img = Image.fromarray(open_cv_image)



        # output_img is an PIL image
        output_img = img

        output_str = pil_image_to_base64(output_img)

        # convert eh base64 string in ascii to base64 string in _bytes_
        #print(output_str)
        self.to_output = output_str.decode("utf-8")

        print("output"+self.to_output)

    def keep_processing(self):
        if(len(self.to_process) > 0):
            self.process_one()
            sleep(0.01)
        else:
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process = input
        print("camin: " + self.to_process)


    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        print("camout: "+self.to_output)
        return self.to_output.encode("utf-8")

'''
video_capture = cv2.VideoCapture(0)  # Capture video from webcam 0
while True:
    ret, frame = video_capture.read()
    frame = FaceRcecognition(frame, updateinreg=False)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''
