import cv2
from assets.Handlers import FileHandler, ManipulateImage
from utils.env import LoadEnv


class Execute:
    def load_elem(self):
        return LoadEnv.envload()

    def execute(self):
        env = self.load_elem()
        src_img = FileHandler.input_image(env["img_path"])

        ManipulateImage.calc_img_size(src_img)

        FileHandler.display_halt()


if __name__ == "__main__":
    print("OpenCV version: " + cv2.__version__)

    exec = Execute()
    exec.execute()
