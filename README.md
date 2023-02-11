# music-score-analysis

[![Python](https://img.shields.io/badge/Python-3.11.0-green.svg)](https://www.python.org/downloads/release/python-3110/)
[![Pip](https://img.shields.io/badge/Pip-22.3.1-green.svg)](https://pip.pypa.io/en/stable/news/#v22-3-1)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7.0-red.svg)](https://opencv.org/opencv-4-7-0/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌱 Overview

Analyze and display the musical scale from the input music score image.

### Scheme:

- 五線譜を Hough 変換と角度限定で検出
- 音符を膨張収縮処理で検出
- 音符の重心座標と五線譜の位置関係で音階を推定

### Demo:

- 入力画像
  ![input_img](https://user-images.githubusercontent.com/63791288/218268392-2c745d44-8ef1-4241-9868-88f6f60ddad2.png)
- 出力画像
  ![result_img](https://user-images.githubusercontent.com/63791288/218268352-b17cfc7e-a5ae-4426-b431-d71a156d6d18.jpg)

## 🚀 Usage

```sh
### [Only after clone] Configure your local environment.
$ make init

### Run this program.
$ make run
```
