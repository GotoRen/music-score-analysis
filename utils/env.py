import os
from dotenv import load_dotenv
from os.path import join, dirname


class LoadEnv:
    def envload():
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), ".env")
        load_dotenv(dotenv_path)
        env = {
            "debug_mode": os.environ.get("DEBUG_MODE"),
            "input_img_path": os.environ.get("INPUT_IMAGE_PATH"),
            "output_img_path": os.environ.get("OUTPUT_IMAGE_PATH"),
        }

        return env
