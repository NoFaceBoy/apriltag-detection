import cv2

text_color = (255, 0, 0)  # red color(rgb)
line_color = (0, 0, 255)  # blue color
dot_color = (0, 255, 0)  # green color
fontScale = 0.5
thickness = 2


def underline_markers(apriltag_results, video_stream):
    for r in apriltag_results:  # underline markers in squares
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(video_stream, ptA, ptB, line_color, 2)
        cv2.line(video_stream, ptB, ptC, line_color, 2)
        cv2.line(video_stream, ptC, ptD, line_color, 2)
        cv2.line(video_stream, ptD, ptA, line_color, 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(video_stream, (cX, cY), 3, dot_color, 3)
        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        cv2.putText(video_stream, tagFamily, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_DUPLEX, fontScale, text_color, thickness)
        # print("[INFO] tag family: {}".format(tagFamily))
