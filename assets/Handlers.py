import cv2
import numpy as np
import math

WINDOW_NAME_INPUT = "input"
WINDOW_NAME_OUTPUT = "output"

### FileHandler defines basic I/O handling functions.
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


### ManipulateImage defines arbitrary processing on the image.
class ManipulateImage:
    def edge_detection(src_img):
        do2_img = cv2.imread("./img/note/0_do.png", cv2.IMREAD_COLOR)
        do_img = cv2.resize(do2_img, None, None, 0.12, 0.12)

        mask = np.all(do_img[:, :, :] == [0, 0, 0], axis=-1)
        do_img = cv2.cvtColor(do_img, cv2.COLOR_BGR2BGRA)
        do_img[mask, 3] = 0

        # image size calculation
        height, width, channels = src_img.shape
        img_size = height * width
        print(img_size)

        # 白黒画像に変換
        gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
        FileHandler.output_image("gray_img", gray_img)

        # 画像処理では白い部分に物がある扱いになるので, 音符や五線譜が白くなるように白黒反転
        bitwise_gray_img = cv2.bitwise_not(gray_img)
        FileHandler.output_image("bitwise_gray_img", bitwise_gray_img)

        # 大津の２値化で0か255に変換
        retval, threshold_img = cv2.threshold(
            bitwise_gray_img, 240, 255, cv2.THRESH_OTSU
        )
        FileHandler.output_image("threshold_img", threshold_img)

        # 各音符のエッジを検出
        contours, hierarchy = ManipulateImage.find_notes(src_img, threshold_img)

        # エッジから各音符の重心座標を取得
        notes_xy_arr = ManipulateImage.get_scores_xy_array(contours)
        print("xy:", notes_xy_arr)

        # 五線譜の線の高さの配列を取得
        score_lines_rho_arr = ManipulateImage.get_score_lines_rho_array(
            src_img, threshold_img
        )

        score_list = ["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ"]
        # 線の外のドや線と線の間の音符を検出するためにちょっと加工する
        # 五線譜を下から見るために逆順にする
        score_lines_rho_arr.reverse()
        between_lines_length = abs(score_lines_rho_arr[0] - score_lines_rho_arr[1])
        between_lines_half_length = math.floor(between_lines_length / 2)
        score_lines_rho_arr.insert(0, score_lines_rho_arr[0] + between_lines_length)
        # 上のコードの時点で配列に「ドミソシレファ」に当たる高さが入っている．間が足りないので埋める．
        # 方法は線と線の間の長さの半分を各要素に足した値を間に入れる(下から見ていってるからほんとは引く必要があった．)
        score_height_base = []
        for item in score_lines_rho_arr:
            score_height_base.append(item)
            score_height_base.append(item - between_lines_half_length)
        # 最後に一番下のドと同じ立ち位置の一番上のラを追加する
        score_height_base.append(score_height_base[-1] - between_lines_half_length)
        print(score_height_base)
        # 音符がどの線と一番高さが近いかを判定してどの音階か取得
        for note_index, note in enumerate(notes_xy_arr):
            min = 100
            min_index = 0
            for index, height in enumerate(score_height_base):
                diff = abs(height - note[1])  # note[0] = x軸 / note[1] = y軸
                if diff < min:
                    min = diff
                    min_index = index
            print(f"{note_index}番目の音符は, {score_list[min_index%7]}")
            print(f"{note_index}番目の音符は, {note[0]}, {note[1]}")
        ManipulateImage.overlay(src_img, do_img, 71, 374)

        # # retval, dst = cv2.threshold(gray_img, 190, 255, cv2.THRESH_TOZERO_INV)
        # dst = cv2.bitwise_not(dst)
        # retval, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # # ManipulateImage.circle_detection(src_img, dst)

        # # 輪郭抽出
        # cnt, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # # FileHandler.output_image("detect counter", dst)

        # # 抽出領域出力
        # dst = cv2.drawContours(dst, cnt, -1, (255, 255, 255, 255), 2, cv2.LINE_AA)
        # # FileHandler.output_image("score", dst)

        # # kernel = np.ones((5,5),np.uint8)
        # # dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel, iterations=12)
        # # dst = cv2.erode(dst,kernel,iterations = 2)
        # # FileHandler.output_image("bouchou", dst)

        # # ManipulateImage.circle_detection(src_img, dst)

    # find_notes finds hodges in the input image.
    def find_notes(src_img, threshold_img):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dst = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, kernel, iterations=4)

        FileHandler.output_image("dst", dst)

        contours, hierarchy = cv2.findContours(
            dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        dst = cv2.drawContours(src_img, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

        FileHandler.output_image("find_notes", dst)
        return contours, hierarchy

    def get_scores_xy_array(contours):
        arr = []
        for i, cnt in enumerate(contours):
            # 輪郭のモーメントを計算する。
            M = cv2.moments(cnt)
            # モーメントから重心を計算する。
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            arr.append([cx, cy])
        return arr

    # 横線のみを検出してその線のrhoを返す．この場合rhoは実質yと同じとして扱える．（rhoは線と垂直な原点とつなぐ線の長さのため）
    def get_score_lines_rho_array(src_img, threshold_img):
        lines = cv2.HoughLines(threshold_img, 1, np.pi / 180, 300)
        lines = lines.squeeze(axis=1)

        # 直線の角度がほぼ90°(-85° ~ 95°) のものだけ抽出する。
        lines = list(filter(lambda x: abs(x[1] - np.pi / 2) <= np.deg2rad(5), lines))
        print(lines)

        # 直線を描画する。
        def draw_line(img, theta, rho):
            h, w = img.shape[:2]
            if np.isclose(np.sin(theta), 0):
                x1, y1 = rho, 0
                x2, y2 = rho, h
            else:
                calc_y = lambda x: rho / np.sin(theta) - x * np.cos(theta) / np.sin(
                    theta
                )
                x1, y1 = 0, int(calc_y(0))
                x2, y2 = w, int(calc_y(w))

            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        lines_rho_arr = []
        for rho, theta in lines:
            draw_line(src_img, theta, rho)
            lines_rho_arr.append(rho)

        FileHandler.output_image("line_img", src_img)

        return lines_rho_arr

    def overlay(back_img, fore_img, x, y):
        # shift_x, shift_y = (0, 0)

        # fore_h, fore_w = fore_img.shape[:2]
        # fore_x_min, fore_x_max = 0, fore_w
        # fore_y_min, fore_y_max = 0, fore_h

        # back_h, back_w = back_img.shape[:2]
        # back_x_min, back_x_max = shift_y, shift_y + fore_h
        # back_y_min, back_y_max = shift_x, shift_x + fore_w

        # if back_x_min < 0:
        #     fore_x_min = fore_x_min - back_x_min
        #     back_x_min = 0

        # if back_x_max > back_w:
        #     fore_x_max = fore_x_max - (back_x_max - back_w)
        #     back_x_max = back_w

        # if back_y_min < 0:
        #     fore_y_min = fore_y_min - back_y_min
        #     back_y_min = 0

        # if back_y_max > back_h:
        #     fore_y_max = fore_y_max - (back_y_max - back_h)
        #     back_y_max = back_h

        # back_img[back_y_min:back_y_max, back_x_min:back_x_max] = fore_img[
        #     fore_y_min:fore_y_max, fore_x_min:fore_x_max
        # ]
        dx = x - 50  # 横方向の移動距離
        dy = y - 50  # 縦方向の移動距離
        h, w = fore_img.shape[:2]
        back_img[dy : dy + h, dx : dx + w] = fore_img

        FileHandler.output_image("over_lay", back_img)

    # def musical_scale_definition:


# def circle_detection(src_img, gray_img):
#     circles = cv2.HoughCircles(
#         gray_img,
#         cv2.HOUGH_GRADIENT,
#         dp=1.5,
#         minDist=100,
#         maxRadius=100,
#         param1=100,
#         param2=25,
#     )
#     print(circles)
#     for c in circles[0, :]:
#         # 円周を描画する
#         cv2.circle(
#             src_img,
#             (int(c[0]), int(c[1])),
#             int(c[2]),
#             (
#                 0,
#                 0,
#                 165,
#             ),
#         )
#     FileHandler.output_image("detect cirecle", src_img)

# def five_lines_detection(src_img):
#     gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
#     line_retval, line_dst = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)
#     line_dst = cv2.bitwise_not(line_dst)
#     cv2.HoughLinesP()
