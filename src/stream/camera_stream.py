from pupil_apriltags import Detector
import numpy as np
import cv2
from src.markers.underline_markers import underline_markers
import src.config.config as conf
from src.markers.screen_corner import get_marker_location
from src.stream.tag_location_detection import TagDetection


def web_stream():
    pipeline = conf.camera_config()
    detector = Detector(families=conf.apriltag_config())
    detection = TagDetection()
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
        get_marker_location(results, (640, 480))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', rgb_image)[1].tobytes() + b'\r\n')
