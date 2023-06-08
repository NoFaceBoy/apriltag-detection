def get_marker_location(result, resolution):
        marker_center = result.center
        image_center = (resolution[0] / 2, resolution[1] / 2)
        if marker_center[0] < image_center[0] + 50 and marker_center[0] < image_center[0] - 50 and marker_center[1] < image_center[1] + 50 and marker_center[1] < image_center[1] - 50:
            return"Left top corner"

        if marker_center[0] > image_center[0] + 50 and marker_center[0] > image_center[0] - 50 and marker_center[1] < image_center[0] + 50 and marker_center[1] < image_center[1] - 50:
            return "Right top corner"

        if marker_center[0] < image_center[0] + 50 and marker_center[0] < image_center[0] - 50 and marker_center[1] > image_center[1] + 50 and marker_center[1] > image_center[1] - 50:
            return "Left bottom corner"

        if marker_center[0] > image_center[0] + 50 and marker_center[0] > image_center[0] - 50 and marker_center[0] > image_center[1] + 50 and marker_center[1] > image_center[1] - 50:
            return "Right bottom corner"

        if image_center[0] + 50 >= marker_center[0] >= image_center[0] - 50 and image_center[1] + 50 >= marker_center[1] >= image_center[1] - 50:
            return "Center"

        return ""
