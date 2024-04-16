import cv2
import numpy as np
import argparse

class KeypointClicker:
    def __init__(self, window_name: str = "KeypointClicker"):
        self._keypoints = []
        self._window_name = window_name
        self._image = None

    # Callback function, such that we collect the left mouse-click
    # Draws circle and saves clicked keypoints
    def draw_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self._image, (x,y), 5, (255,0,0), -1)
            self._keypoints.append([x, y])
            print(f'X: {x}, Y: {y}')

    # Generate a copy of the image and visualize the clicked keypoints
    # Returns a list of (x, y) coordinates that have been clicked
    # Press ESC to close the windo
    def click_keypoints(self, image: np.array):
        self._keypoints = []
        self._image = image.copy()
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self.draw_circle)

        while(1):
            cv2.imshow(self._window_name, self._image)
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
        
        cv2.destroyWindow(self._window_name)
        return self._keypoints


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open arbitrary video with TAP.")
    parser.add_argument("-i", "--input", help="Input video", default="test.mp4")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.input)
    _, first_frame = cap.read()
    kp_clicker = KeypointClicker()

    keypoints = kp_clicker.click_keypoints(first_frame)
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('Inputvideo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()