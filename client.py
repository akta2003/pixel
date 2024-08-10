import socketio
import base64
import eventlet
import cv2

sio = socketio.Client()

# Inisialisasi kamera USB eksternal
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

@sio.on('connect')
def on_connect():
    print("Connected to server.")

@sio.on('disconnect')
def on_disconnect():
    print("Disconnected from server.")

@sio.on('receive')
def terima_pesan(sid,data):
    print('Pesan diterima dari server:', data)

def send_video():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert the frame to JPEG format
        _, encoded_frame = cv2.imencode('.jpg', frame)
        # Convert the JPEG frame to base64-encoded string
        data = base64.b64encode(encoded_frame).decode('utf-8')

        # Send the video frame to the server over Socket.IO
        sio.emit('stream_video', data)

        # Delay for a short interval before sending the next frame
        eventlet.sleep(0.1)

    camera.release()
    print("Camera disconnected.")


while True:
    try:
        sio.connect('http://192.168.1.102:5001')
        send_video()
    except Exception as error:
        print(error)
