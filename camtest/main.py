import cv2


count = 0


def open_cameras(cameras):
    caps = []
    for cam_index in cameras:
        cap = cv2.VideoCapture(cam_index)
        caps.append(cap)

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Camera {i}", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # if s is pressed
        #
        if cv2.waitKey(1) & 0xFF == ord("s"):
            for i, cap in enumerate(caps):
                cap.release()
                cv2.destroyAllWindows()

    for cap in caps:
        cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    cameras = [2, 3]
    if cameras:
        print(f"Available cameras: {cameras}")
        open_cameras(cameras)
    else:
        print("No cameras detected")
