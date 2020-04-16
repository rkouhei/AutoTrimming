# ライブラリの読み込み
from func import noise_removal, trap_cor, trim, trim_one
import cv2
import numpy as np
from PIL import Image

# 画像パス
IMG = "./data/resize.JPG"
# IMG = "./data/resize2.JPG"

if __name__ == "__main__" :
  # 画像の読み込み
  img = cv2.imread(IMG)

  # while True :
  imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  ret,thresh = cv2.threshold(imgray,127,255,0)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  area = []
  for c in contours :
    area.append(cv2.contourArea(c))
  # print(area.index(max(area)))
  max_index = area.index(max(area))
  epsilon = 0.1 * cv2.arcLength(contours[max_index], True)
  tmp = cv2.approxPolyDP(contours[max_index], epsilon, True)

  # img2 = cv2.drawContours(img, contours, 0, (0,255,0), 3)
  top_l = tmp[0][0][0] if tmp[0][0][0] > tmp[1][0][0] else tmp[1][0][0]
  und_l = tmp[2][0][0] if tmp[2][0][0] < tmp[3][0][0] else tmp[3][0][0]
  und_r = tmp[1][0][1] if tmp[1][0][1] < tmp[2][0][1] else tmp[2][0][1]
  top_r = tmp[0][0][1] if tmp[0][0][1] > tmp[3][0][1] else tmp[0][0][1]
  print(tmp)
  # print(top_r,und_r, top_r,und_l)
  img2 = img[top_r:und_r, top_r:und_l]
  # imgray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
  # dst = cv2.Canny(imgray, 0.0, 250.0)

  dst = cv2.inRange(img2, (0, 0, 0), (250, 250, 250))

  # 微分
  sobelx64f = cv2.Sobel(dst,cv2.CV_64F,1,0,ksize=5)
  abs_sobel64f = np.absolute(sobelx64f)
  sobel_8u = np.uint8(abs_sobel64f)

  contours = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

  # 輪郭の座標をリストに代入していく
  x1 = [] #x座標の最小値
  y1 = [] #y座標の最小値
  x2 = [] #x座標の最大値
  y2 = [] #y座標の最大値
  for i in range(1, len(contours)):# i = 1 は画像全体の外枠になるのでカウントに入れない
    ret = cv2.boundingRect(contours[i])
    x1.append(ret[0])
    y1.append(ret[1])
    x2.append(ret[0] + ret[2])
    y2.append(ret[1] + ret[3])

  # 輪郭の一番外枠を切り抜き
  x1_min = min(x1)
  y1_min = min(y1)
  x2_max = max(x2)
  y2_max = max(y2)
  # cv2.rectangle(img, (x1_min, y1_min), (x2_max, y2_max), (0, 255, 0), 3)

  trim_img = img2[y1_min:y2_max, x1_min:x2_max]
  # trim_img = cv2.drawContours(img2, contours, -1, (0,255,0), 3)
  cv2.imshow('trim', trim_img)

  # lines = cv2.HoughLinesP(sobel_8u, rho=1, theta=np.pi/360, threshold=80, minLineLength=600, maxLineGap=75)
  # print(lines)
  # for line in lines:
  #   x1, y1, x2, y2 = line[0]

  #   # 赤線を引く
  #   red_line_img = cv2.line(img2, (x1,y1), (x2,y2), (0,0,255), 3)
  # cv2.imshow('red', red_line_img)

  # corners = cv2.goodFeaturesToTrack(dst, 50, 0.01, 20.0, blockSize=5, useHarrisDetector=False)
  # print(corners)

  # for i in corners :
  #   x, y = i.ravel()
  #   cv2.circle(img2, (x, y), 4, (255, 0, 0), 2)
  # contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  # cv2.drawContours(img2, contours, -1, (0, 255, 0), 1)

  #白黒反転画像
  # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # マスクを作製して、ノイズの除去

  # 台形補正

  # 画像の中心と回転角度の算出

  # 回転

  # 四隅の座標の算出

  # トリミング


  cv2.imshow('original', img2)
  # cv2.imshow('imgray', imgray)
  cv2.imshow('dst', dst)
  cv2.imshow('sobel', sobel_8u)
  # cv2.imshow('dst2', dst2)

  cv2.waitKey(0)
  cv2.destroyAllWindows()

  # cv2.imwrite('./out/yama.png', img_angle)