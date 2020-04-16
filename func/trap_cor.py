# 画像の台形補正
## ライブラリのインポート
import numpy as np
import cv2

def correction(img) :
  size = img.shape[0] * img.shape[1]
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # 入力座標の選定
  best_white = 0
  best_rate = 0.0
  best_approx = []
  dict_approx = {}
  for white in range(10, 255, 10):
    # 二値化
    ret, th1 = cv2.threshold(gray_img, white, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 面積が以下の条件に満たすものを選定
    # 角の数が4つ、1%以上、99%未満
    max_area = 0
    approxs = []
    for cnt in contours:
      area = cv2.contourArea(cnt)
      epsilon = 0.1 * cv2.arcLength(cnt, True)
      tmp = cv2.approxPolyDP(cnt, epsilon, True)
      if 4 == len(tmp):
        approxs.append(tmp)
        if size * 0.01 <= area\
        and area <= size * 0.99\
        and max_area < area:
          best_approx = tmp
          max_area = area
    if 0 != max_area:
      rate = max_area / size * 100
      if best_rate < rate:
        best_rate = rate
        best_white = white
    dict_approx.setdefault(white, approxs)

  if 0 == best_white:
    print("The analysis failed.")
    exit()

  # 出力座標の計算(三平方の定理)
  r_btm = best_approx[0][0]
  r_top = best_approx[1][0]
  l_top = best_approx[2][0]
  l_btm = best_approx[3][0]
  top_line   = (abs(r_top[0] - l_top[0]) ^ 2) + (abs(r_top[1] - l_top[1]) ^ 2)
  btm_line   = (abs(r_btm[0] - l_btm[0]) ^ 2) + (abs(r_btm[1] - l_btm[1]) ^ 2)
  left_line  = (abs(l_top[0] - l_btm[0]) ^ 2) + (abs(l_top[1] - l_btm[1]) ^ 2)
  right_line = (abs(r_top[0] - r_btm[0]) ^ 2) + (abs(r_top[1] - r_btm[1]) ^ 2)
  max_x = top_line  if top_line  > btm_line   else btm_line
  max_y = left_line if left_line > right_line else right_line

  # 画像の座標上から4角を切り出す
  pts1 = np.float32(best_approx)
  pts2 = np.float32([[max_x, max_y], [max_x, 0], [0, 0], [0, max_y]])

  # 透視変換の行列を求める
  M = cv2.getPerspectiveTransform(pts1, pts2)

  # 変換行列を用いて画像の透視変換
  dst = cv2.warpPerspective(img, M, (max_x, max_y))

  return dst