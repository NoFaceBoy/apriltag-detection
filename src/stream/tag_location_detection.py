from pupil_apriltags import Detector
import numpy as np
import cv2
import src.config.config as conf
from src.markers.screen_corner import get_marker_location


class TagDetection:
    def __init__(self):
        self.pipeline = conf.camera_config()
        self.detector = Detector(families=conf.apriltag_config())

    def detect(self) -> str | None:
        aligned_image = False
        while not aligned_image:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            else:
                aligned_image = True

        color_image = np.asanyarray(color_frame.get_data())

        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        self.detector.detect(gray)
        results = self.detector.detect(gray)
        if not results:
            return None
        results = results[0]
        return get_marker_location(results, conf.RESOLUTION)
