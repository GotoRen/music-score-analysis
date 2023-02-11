import cv2
from assets.Handlers import FileHandler, ManipulateImage
from utils.env import LoadEnv

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"

env = LoadEnv.envload()


class Execute:
    def execute(self):
        ### 入力
        input_img = FileHandler.input_image(env["input_img_path"])
        FileHandler.disp_image(WINDOW_NAME_INPUT, input_img)

        ### 処理
        result_img = ManipulateImage.edge_detection(input_img)
        FileHandler.disp_image(WINDOW_NAME_OUTPUT, result_img)

        ### 保存
        FileHandler.save_to_image(env["output_img_path"], input_img)

        ### 停止
        FileHandler.disp_halt()


if __name__ == "__main__":
    print("[INFO] OpenCV version: " + cv2.__version__)

    exec = Execute()
    exec.execute()
