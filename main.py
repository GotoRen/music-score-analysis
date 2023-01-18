"""This is a main program."""
import cv2

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"

# pip3 install opencv-python
path = "img/sample.png"
img = cv2.imread(path)
print(cv2.__version__)

cv2.imshow(WINDOW_NAME_OUTPUT, img)
cv2.waitKey(0)
cv2.destroyAllWindows()
