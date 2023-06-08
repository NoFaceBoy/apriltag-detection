from pupil_apriltags import Detector
import numpy as np
import cv2
from markers.underline_markers import underline_markers
import config.config as conf


def web_stream():
    pipeline = conf.camera_config()
    detector = Detector(families=conf.apriltag_config())

    while True:
        aligned_image = False
        while not aligned_image:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            else:
                aligned_image = True

        color_image = np.asanyarray(color_frame.get_data())

        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        detector.detect(gray)
        results = detector.detect(gray)
        rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        underline_markers(results, rgb_image)
        cv2.waitKey(1)
        print(results)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', rgb_image)[1].tobytes() + b'\r\n')
