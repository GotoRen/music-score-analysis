import cv2

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"
WINDOW_NAME_OUTPUT = "debug"


class FileHandler:
    def input_image(path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        FileHandler.output_image(WINDOW_NAME_INPUT, img)
        return img

    def output_image(window_name, img):
        cv2.imshow(window_name, img)

    def save_to_image():
        print("saving image...")

    def disp_halt():
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class ManipulateImage:
    def calc_img_size(src_img):
        height, width, channels = src_img.shape
        img_size = height * width
        print(img_size)

        gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
        FileHandler.output_image(WINDOW_NAME_OUTPUT, gray_img)
