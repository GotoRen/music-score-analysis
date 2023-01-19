import cv2
from assets.Handlers import FileHandler
from utils.env import LoadEnv


class Execute:
    def load_elem(self):
        return LoadEnv.envload()

    def execute(self):
        env = self.load_elem()
        input_img = FileHandler.input_image(env["img_path"])
        FileHandler.output_image(input_img)


if __name__ == "__main__":
    print("OpenCV version: " + cv2.__version__)

    exec = Execute()
    exec.execute()
