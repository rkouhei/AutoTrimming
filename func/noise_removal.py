# 画像のノイズ除去
## ライブラリのインポート
import numpy as np
import cv2

def opening(img) :
  kernel = np.ones((5, 5), np.uint8)
  dst_open = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
  return dst_open

def median(img) :
  k_size = 3
  dst_mask = cv2.medianBlur(img, k_size)
  return dst_mask


def remove(img) :
  dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
  return dst