import cv2

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"


class FileHandler:
    def input_image(path):
        img = cv2.imread(path)
        return img

    def output_image(img):
        cv2.imshow(WINDOW_NAME_OUTPUT, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
