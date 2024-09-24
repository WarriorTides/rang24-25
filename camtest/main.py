# import cv2


# count = 0


# def open_cameras(cameras):
#     caps = []
#     cam_index = 0
#     # for cam_index in cameras:
#     cap = cv2.VideoCapture(cam_index)
#         # caps.append(cap)

#     while True:
#         for i, cap in enumerate(caps):
#             ret, frame = cap.read()
#             if ret:
#                 cv2.imshow(f"Camera {i}", frame)

#         # Press 'q' to exit
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#         # if s is pressed
#         #
#         if cv2.waitKey(1) & 0xFF == ord("s"):
#             for i, cap in enumerate(caps):
#                 cap.release()
#                 cv2.destroyAllWindows()
#             cam_index = (cam_index + 1) % len(cameras)
#             cameras = [cam_index]
#             open_cameras(cameras)

#     # for cap in caps:
#     cap.release()

#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     cameras = [0, 1]
#     if cameras:
#         print(f"Available cameras: {cameras}")
#         open_cameras(cameras)
#     else:
#         print("No cameras detected")

import cv2

count = 0

def open_cameras(cameras):
    caps = []
    cam_index = 0
    def set_resolution(cap):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Open the first pair of cameras and set resolution
    cap = cv2.VideoCapture(cameras[cam_index])
    set_resolution(cap)
    
    cap2 = cv2.VideoCapture(cameras[cam_index + 1])
    set_resolution(cap2)
    caps.append(cap)
    caps.append(cap2)
    

    while True:
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        if ret:
            cv2.imshow(f"Camera {cameras[cam_index]}", frame)
        if ret2:
            cv2.imshow(f"Camera {cameras[cam_index + 1]}", frame2)
        
        key = cv2.waitKey(1) & 0xFF

        # Press 'q' to exit
        if key == ord("q"):
            break

        # Press 's' to switch camera
        if key == ord("s"):
            # Release the current camera and close the window
            for cap in caps:
                cap.release()
            cv2.destroyAllWindows()

            # Move to the next camera index (loop around if necessary)
            cam_index = (cam_index + 2) % len(cameras)

            # Open the next camera
            caps = []
            cap = cv2.VideoCapture(cameras[cam_index])
            set_resolution(cap)
            caps.append(cap)
            cap2 = cv2.VideoCapture(cameras[cam_index + 1])
            set_resolution(cap2)
            caps.append(cap2)
    

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cameras = [0, 1, 2, 3]  # List of camera indices
    if cameras:
        print(f"Available cameras: {cameras}")
        open_cameras(cameras)
    else:
        print("No cameras detected")
