import pyrealsense2 as rs

RESOLUTION = (640, 480)


def camera_config():
    while True:
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("Depth camera with Color sensor not found")
            exit(0)

        config.enable_stream(rs.stream.depth, RESOLUTION[0], RESOLUTION[1], rs.format.z16, 30)
        config.enable_stream(rs.stream.color, RESOLUTION[0], RESOLUTION[1], rs.format.rgb8, 30)

        pipeline.start(config)
        return pipeline


def apriltag_config():
    family = "36h11"  # recommended 36h11; (16h5, Circle21h7, 25h9, Standard41h12, Custom48h12, Circle49h12, Standard52h13)
    tag_family = f"tag{family}"
    return tag_family
