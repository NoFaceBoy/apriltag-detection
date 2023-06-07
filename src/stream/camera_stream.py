import pyrealsense2 as rs
from pupil_apriltags import Detector
import numpy as np
import cv2
from markers.underline_markers import underline_markers


def stream():
    config = rs.config()
    pipeline = rs.pipeline()

    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == "RGB Camera":
            found_rgb = True
            break
    if not found_rgb:
        print("Depth camera with Color sensor not found")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

    pipeline.start(config)

    detector = Detector(families="tag36h11")

    while True:

        aligned_image = False
        while not aligned_image:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            else:
                aligned_image = True

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # For stream in window mode.
        # depth_colormap = cv2.applyColorMap(
        #     cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #
        # color_colormap_dim = color_image.shape
        # depth_colormap_dim = depth_colormap.shape
        #
        # if color_colormap_dim != depth_colormap_dim:
        #     resized_color_image = cv2.resize(
        #         color_image,
        #         dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
        #         interpolation=cv2.INTER_AREA,
        #     )
        #     images = np.hstack((resized_color_image, depth_colormap))
        # else:
        #     images = np.hstack((color_image, depth_colormap))

        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        detector.detect(gray)
        results = detector.detect(gray)
        rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        underline_markers(results, rgb_image)
        cv2.waitKey(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', rgb_image)[1].tobytes() + b'\r\n')
