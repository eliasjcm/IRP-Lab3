import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage import io
from google.colab.patches import cv2_imshow

img = io.imread("https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png?20111103160805")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(img_gray)

def tiene_mapeo(a: complex, b: complex, c: complex, d: complex):
  print(f"{b}*{c}-{a}*{d}={b*c-a*d}")
  return b*c-a*d != complex(0,0)
  
def crear_mapeo(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def crear_mapeo_inverso(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def mapear_imagen(img, a, b, c, d):
  mapeo = crear_mapeo(a, b, c, d)
  mapeo_inverso = crear_mapeo_inverso(a, b, c, d)
  width, height = img.shape
  print(img.shape)
  new_img = np.zeros((width, height), np.uint8)
  for x in range(width):
    for y in range(height):
      w = mapeo(complex(x, y))
      # if ()
      new_x = int(w.real)
      new_y = int(w.imag)
      # print(new_x, new_y)
      if 0 <= new_x < width and 0 <= new_y < height:
        new_img[new_x][new_y] = img[x,y]

    bordesX[fila_actual] = min, max min<pixel<max
  for x in range(width):
    
    for y in range(height):
      w = mapeo(complex(x, y))
      # if ()
      new_x = int(w.real)
      new_y = int(w.imag)
      # print(new_x, new_y)
      if 0 <= new_x < width and 0 <= new_y < height:
        new_img[new_x][new_y] = img[x,y]

    
        # new_img[new_x][new_y] = 255
  return new_img

mapeada = mapear_imagen(img_gray, 2.1+2.1j, 0, 0.003, 1+1j)
# mapeada = mapear_imagen(img_gray, 0+.75j, 0, 0, 1)
plt.imshow(mapeada)

cv2_imshow(mapeada)