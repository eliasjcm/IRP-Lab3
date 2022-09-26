import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
# from skimage import io
# from google.colab.patches import cv2_imshow

img = cv2.imread('lenna.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def tiene_mapeo(a: complex, b: complex, c: complex, d: complex):
  print(f"{b}*{c}-{a}*{d}={b*c-a*d}")
  return b*c-a*d != complex(0,0)
  
def crear_mapeo(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def crear_mapeo_inverso(a, b, c, d):
  return lambda w : (-d*w + b) / (c*w - a)

def interpolacion4(img, x, y):
  count = 0
  value = img[x, y-1]
  count += value
  value = img[x, y+1]
  count += value
  value = img[x-1, y]
  count += value
  value = img[x+1, y]
  count += value
  count = count / 4
  return count

def interpolacion8(img, x, y):
  count = 0
  value = img[x, y-1]
  count += value
  value = img[x, y+1]
  count += value
  value = img[x-1, y]
  count += value
  value = img[x+1, y]
  count += value
  value = img[x-1, y-1]
  count += value
  value = img[x-1, y+1]
  count += value
  value = img[x+1, y-1]
  count += value
  value = img[x+1, y+1]
  count += value
  count = count / 8
  return count

def new_size(img, a, b, c, d):
  mapeo = crear_mapeo(a, b, c, d)
  width, height = img.shape
  new_width, new_height = 0, 0

  for x in [0, 1, width-2, width-1]:
    for y in range(height):
      w = mapeo(complex(x, y))
      new_x = int(w.real)
      new_y = int(w.imag)
      new_width = max(new_width, new_x)
      new_height = max(new_height, new_y)
    
  for y in [0, 1, height-2, height-1]:
    for x in range(width):
      w = mapeo(complex(x, y))
      new_x = int(w.real)
      new_y = int(w.imag)
      new_width = max(new_width, new_x)
      new_height = max(new_height, new_y)
    
  return new_width, new_height

def newImage(img, a, b, c, d):
  new_width, new_height = new_size(img, a, b, c, d)
  mapeo = crear_mapeo_inverso(a, b, c, d)
  new_img = np.zeros((new_width, new_height), np.uint8)
  # new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)

  for x in range(new_width):
    for y in range(new_height):
      z = mapeo(complex(x, y))
      new_x = int(z.real)
      new_y = int(z.imag)
      # print("Forma2", x, y, new_x, new_y)
      if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
        new_img[x, y] = img[new_x, new_y]   
  return new_img

def newImageInterAux(img, a, b, c, d, inter8):
  new_width, new_height = new_size(img, a, b, c, d)
  mapeo = crear_mapeo_inverso(a, b, c, d)
  new_img = np.zeros((new_width, new_height), np.uint8)
  # new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)

  for x in range(new_width):
    for y in range(new_height):
      z = mapeo(complex(x, y))
      new_x = int(z.real)
      new_y = int(z.imag)
      # print("Forma2", x, y, new_x, new_y)
      if not (new_x == 0 or new_x == (img.shape[0]-1) or new_y == 0 or new_y == (img.shape[0]-1)):
        if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
          if inter8:
            new_img[x, y] = interpolacion8(img, new_x, new_y)
          else:
            new_img[x, y] = interpolacion4(img, new_x, new_y)
  return new_img

def newImageInterpolation4(img, a, b, c, d):
  new_img = newImageInterAux(img, a, b, c, d, False)
  return new_img

def newImageInterpolation8(img, a, b, c, d):
  new_img = newImageInterAux(img, a, b, c, d, True)
  return new_img

def addGaussianBlur(img, range):
  img = cv2.GaussianBlur(img, (range, range), 0)
  return img

new_img = newImage(img_gray, 6, 0, 0, 1)

plt.imshow(new_img)
plt.show()

cv2.imwrite("Test.png", new_img)

# cv2_imshow(mapeada)