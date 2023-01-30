import cv2
from assets.handlers import FileHandler, ManipulateImage
from utils.env import LoadEnv
import sys


class Execute:
    def load_elem(self):
        return LoadEnv.envload()

    def execute(self):
        env = self.load_elem()
        src_img = FileHandler.input_image(env["input_img_path"])

        ManipulateImage.edge_detection(src_img)
        # ManipulateImage.five_lines_detection(src_img)

        FileHandler.disp_halt()
        FileHandler.save_to_image(env["output_img_path"], src_img)


if __name__ == "__main__":
    print(sys.executable)
    print("[INFO] OpenCV version: " + cv2.__version__)

    exec = Execute()
    exec.execute()
