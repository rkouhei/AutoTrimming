# ライブラリの読み込み
from func import noise_removal, trap_cor, trim, trim_one
import cv2
import numpy as np
from PIL import Image

# 画像パス
# IMG = "./data/EPSON001.JPG"
# IMG = "./data/Lenna.bmp"
# IMG = "./data/test.JPG"
IMG = "./data/resize.JPG"

if __name__ == "__main__" :
  # 画像の読み込み
  img = cv2.imread(IMG)
  #白黒反転画像
  img2 = cv2.bitwise_not(img)

  # マスクを作製して、ノイズの除去
  # dst = noise_removal.remove(img)
  # dst_mask = noise_removal.median(img)
  # dst_open = noise_removal.opening(img)

  # 台形補正
  dst = trap_cor.correction(img)
  cv2.imshow('dst', dst)
  imgray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  ret,thresh = cv2.threshold(imgray,100,255,0)
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  im_con = img.copy()
  cv2.drawContours(im_con, contours, -1, (0,255,0), 2)
  cv2.imshow('im_con', im_con)

  # 画像の中心と回転角度の算出

  # 回転

  # 四隅の座標の算出

  # トリミング
  
  # 見てみる
  # cv2.imshow('img', img)
  # cv2.imshow('dst2', dst2)
  # cv2.imshow('dst_mask', dst_mask)
  # cv2.imshow('dst_open', dst_open)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
  # cv2.imwrite('./out/dst2_image.JPG', dst2)

  # trim_one.trimImage(Image.open(IMG), 'trim_' + IMG)

  # 
  res = trim.trim_img(dst)

  # 画像の角度修正(tmp)
  # 高さ取得
  height = res.shape[0]
  # 幅を取得
  width = res.shape[1]  
  # 画像の中心を取得
  center = (int(width/2), int(height/2))
  # 回転する角度
  angle = 180.0
  #スケールを指定
  scale = 1.0
  #getRotationMatrix2D関数を使用
  trans = cv2.getRotationMatrix2D(center, angle , scale)
  #アフィン変換
  img_angle = cv2.warpAffine(res, trans, (width,height))

  # cv2.imshow('result', res)
  cv2.imshow('original', img)
  cv2.imshow('original2', img2)
  cv2.imshow('angle', img_angle)
  cv2.imwrite('/out/yama.png', img_angle)

  cv2.waitKey(0)
  cv2.destroyAllWindows()

  # cv2.imwrite('./out/yama.png', img_angle)