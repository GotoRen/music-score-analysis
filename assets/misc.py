import numpy as np
from PIL import Image, ImageDraw, ImageFont


class PillowMisc:
    def pil2cv(imgPIL):
        imgCV_RGB = np.array(imgPIL, dtype=np.uint8)
        imgCV_BGR = np.array(imgPIL)[:, :, ::-1]
        return imgCV_BGR

    def cv2pil(imgCV):
        imgCV_RGB = imgCV[:, :, ::-1]
        imgPIL = Image.fromarray(imgCV_RGB)
        return imgPIL

    def put_text(img, text, org, fontFace, fontScale, color):
        x, y = org
        b, g, r = color
        colorRGB = (r, g, b)
        imgPIL = PillowMisc.cv2pil(img)
        draw = ImageDraw.Draw(imgPIL)  # ImageDraw.text() の xy は右上基準
        fontPIL = ImageFont.truetype(font=fontFace, size=fontScale)
        draw.text(xy=(x, y), text=text, fill=colorRGB, font=fontPIL)
        imgCV = PillowMisc.pil2cv(imgPIL)
        return imgCV
