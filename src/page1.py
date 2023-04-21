import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# capture frames from the webcam
camera = cv2.VideoCapture(0)

run_camera = True


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/shutdown')
def shutdown():
    camera.release()
    cv2.destroyAllWindows()
    return 'Shutting down...'


if __name__ == '__main__':
    app.run(debug=True)
