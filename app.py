from sys import stdout
from makeup_artist import Makeup_artist
import logging
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, join_room, leave_room, close_room, rooms, disconnect
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
import imghdr
import os
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from camera import Process
#from flask_login import current_user

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
UPLOAD_PATH = 'FaceRecognition/images'
async_mode = None
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app , async_mode=async_mode)
camera = Camera(Makeup_artist())

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


@socketio.on('input image', namespace='/test')
def test_message(input):
    #print("INPUT "+input)
    input = input.split(",")[len(input.split(","))-1]
    image_data = Process(input)
    #image_data = process()
    image_data = image_data.decode("utf-8")
    image_data = "data:image/jpeg;base64," + image_data
    print("OUTPUT " + image_data)
    emit('out-image-event', {'image_data': image_data}, namespace='/test')
    #camera.enqueue_input(input)
    #camera.keep_processing()


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")


@app.route('/')
def faceSteam():
    """Video streaming home page."""
    return render_template('browsePage.html')

@app.route('/faceDetection')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in UPLOAD_EXTENSIONS:
            abort(400)
        uploaded_file.save(os.path.join(UPLOAD_PATH, filename))
    return redirect(url_for('index'))


'''def gen():
    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        #socketio.emit('news', {'processingStatus': 'Started'}, namespace='/test')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def process():
    print("starting to generate frames!")
    frame = camera.get_frame()  # pil_image_to_base64(camera.get_frame())
    print("frame returned")
    return frame

'''
'''
@socketio.on('output image', namespace='/test')
def process_out():
    print("Proccessed")
    image_data = process()
    image_data = image_data.decode("utf-8")
    image_data = "data:image/jpeg;base64,"+image_data
    print("OUTPUT "+image_data)
    socketio.emit('out-image-event', {'image_data': image_data}, namespace='/test')
'''


'''@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

'''


if __name__ == '__main__':
    socketio.run(app)
