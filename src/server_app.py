from flask import Flask, render_template, Response

from stream.camera_stream import web_stream

app = Flask(__name__)


def generate_frames():
    return web_stream()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/depth_video')
def depth_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
