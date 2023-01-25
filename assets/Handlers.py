import cv2

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"


class FileHandler:
    def input_image(src_path):
        img = cv2.imread(src_path, cv2.IMREAD_COLOR)
        FileHandler.output_image(WINDOW_NAME_INPUT, img)
        return img

    def output_image(window_name, img):
        cv2.imshow(window_name, img)

    def save_to_image(dst_path, img):
        print("[INFO] saving image...")
        cv2.imwrite(dst_path, img)

    def disp_halt():
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class ManipulateImage:
    def edge_detection(src_img):

        # image size calculation
        height, width, channels = src_img.shape
        img_size = height * width
        print(img_size)

        # grayscale conversion
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
        # FileHandler.output_image(WINDOW_NAME_DEBUG, gray_img)

        retval, dst = cv2.threshold(gray_img, 190, 255, cv2.THRESH_TOZERO_INV)
        dst = cv2.bitwise_not(dst)
        retval, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        ManipulateImage.circle_detection(src_img, dst)

        # 輪郭抽出
        cnt, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        FileHandler.output_image("detect counter", dst)

        # 抽出領域出力
        dst = cv2.drawContours(dst, cnt, -1, (255, 255, 255, 255), 2, cv2.LINE_AA)
        FileHandler.output_image("score", dst)

    def circle_detection(src_img, gray_img):
        circles = cv2.HoughCircles(
            gray_img,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            maxRadius=100
            param1=100,
            param2=60,
        )
        for c in circles[0, :]:
            print(c)
            # 円周を描画する
            cv2.circle(
                src_img,
                (int(c[0]), int(c[1])),
                int(c[2]),
                (
                    0,
                    0,
                    165,
                ),
            )
            FileHandler.output_image("detect cirecle", src_img)

    # def five_lines_detection(src_img):
    #     gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
    #     line_retval, line_dst = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)
    #     line_dst = cv2.bitwise_not(line_dst)
    #     cv2.HoughLinesP()
