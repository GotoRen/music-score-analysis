import cv2
import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFont


class PillowMisc:
    def cv2_putJPText(
        img,
        text,
        org,
    ):
        print("[INFO] PIL version: " + PIL.__version__)

        fontFace = (cv2.FONT_HERSHEY_SIMPLEX,)
        fontScale = (10,)
        color = ((255, 0, 0),)
        mode = (0,)
        """
        - img: inputするOpenCVの画像
        - text: 挿入する日本語テキスト
        - org: テキストを配置する座標
        - fontFace: フォント
        - fontScale:フ ォントの大きさ。デフォルトは小さめの10。
        - color:R GBのタプルで指定。デフォルトは赤。
        - mode: orgで指定するテキスト描画座標の基準。デフォルトでは左下。0=左下 1=左上 2=中央
        """

        # テキスト描写域を取得
        fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
        dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
        text_w, text_h = dummy_draw.textsize(text, font=fontPIL)
        text_b = int(0.1 * text_h)  # バグにより下にはみ出る分の対策

        # テキスト描写域の左上座標を取得（元画像の左上を原点とする）
        x, y = org
        offset_x = [0, 0, text_w // 2]
        offset_y = [text_h, 0, (text_h + text_b) // 2]
        x0 = x - offset_x[mode]
        y0 = y - offset_y[mode]
        img_h, img_w = img.shape[:2]

        # 画面外なら何もしない
        if not ((-text_w < x0 < img_w) and (-text_b - text_h < y0 < img_h)):
            print("out of bounds")
            return img

        # テキスト描写域の中で元画像がある領域の左上と右下（元画像の左上を原点とする）
        x1, y1 = max(x0, 0), max(y0, 0)
        x2, y2 = min(x0 + text_w, img_w), min(y0 + text_h + text_b, img_h)

        # テキスト描写域と同サイズの黒画像を作り、それの全部もしくは一部に元画像を貼る
        text_area = np.full((text_h + text_b, text_w, 3), (0, 0, 0), dtype=np.uint8)
        text_area[y1 - y0 : y2 - y0, x1 - x0 : x2 - x0] = img[y1:y2, x1:x2]

        # それをPIL化し、フォントを指定してテキストを描写する（色変換なし）
        imgPIL = Image.fromarray(text_area)
        draw = ImageDraw.Draw(imgPIL)
        draw.text(xy=(0, 0), text=text, fill=color, font=fontPIL)

        # PIL画像をOpenCV画像に戻す（色変換なし）
        text_area = np.array(imgPIL, dtype=np.uint8)

        # 元画像の該当エリアを、文字が描写されたものに更新する
        img[y1:y2, x1:x2] = text_area[y1 - y0 : y2 - y0, x1 - x0 : x2 - x0]

        return img
