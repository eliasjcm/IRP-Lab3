import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
# from skimage import io
# from google.colab.patches import cv2_imshow

img = cv2.imread('lenna.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(img_gray)

def tiene_mapeo(a: complex, b: complex, c: complex, d: complex):
  print(f"{b}*{c}-{a}*{d}={b*c-a*d}")
  return b*c-a*d != complex(0,0)
  
def crear_mapeo(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def crear_mapeo_inverso(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def bordes(img, a, b, c, d):


  
  mapeo = crear_mapeo(a, b, c, d)
  width, height = img.shape
  print(img.shape)
  bordes = [[0, 0], {}, {}]
  print(bordes)
  # new_img = np.zeros((width, height), np.uint8)
  # for y in [0, height-1]:
  #   for x in range(width):
  #     w = mapeo(complex(x, y))
  #     new_x = int(w.real)
  #     new_y = int(w.imag)

  #     # print(new_x, new_y)

  #     if new_x not in bordes[1]:
  #       bordes[1][new_x] = [new_y, new_y]
  #     else:
  #       bordes[1][new_x][1] = new_y

  #     if new_y not in bordes[2]:
  #       bordes[2][new_y] = [new_x, new_x]
  #     else:
  #       if new_x < bordes[2][new_y][0]:
  #         bordes[2][new_y][0] = new_x
  #       elif new_x > bordes[2][new_y][1]:
  #         bordes[2][new_y][1] = new_x

  #     bordes[0][0] = max(bordes[0][0], new_x)
  #     bordes[0][1] = max(bordes[0][1], new_y)

  

  for y in [0, height-1]:
    for x in range(width):
      w = mapeo(complex(x, y))
      new_x = int(w.real)
      new_y = int(w.imag)

      # print(new_x, new_y)

      if new_x not in bordes[1]:
        bordes[1][new_x] = [new_y, new_y]
      else:
        bordes[1][new_x][1] = new_y

      if new_y not in bordes[2]:
        bordes[2][new_y] = [new_x, new_x]
      else:
        if new_x < bordes[2][new_y][0]:
          bordes[2][new_y][0] = new_x
        elif new_x > bordes[2][new_y][1]:
          bordes[2][new_y][1] = new_x

      bordes[0][0] = min(bordes[0][0], new_x)
      bordes[0][1] = max(bordes[0][1], new_y)

    
  print(bordes[0])
  print(bordes[1])
  print("\n\n\n")
  print(bordes[2])

    # w = mapeo(complex(x, height-1))

    # if 0 <= new_x < width and 0 <= new_y < height:
    #   new_img[new_x][new_y] = 255
    
  # for y in range(height):
  #   w = mapeo(complex(x, y))
  #   # if ()
  #   new_x = int(w.real)
  #   new_y = int(w.imag)
  #   # print(new_x, new_y)
  #   if 0 <= new_x < width and 0 <= new_y < height:
  #     new_img[new_x][new_y] = img[x,y]

  #   # bordesX[fila_actual] = min, max min<pixel<max
  # for x in range(width):
    
  #   for y in range(height):
  #     w = mapeo(complex(x, y))
  #     # if ()
  #     new_x = int(w.real)
  #     new_y = int(w.imag)
  #     # print(new_x, new_y)
  #     if 0 <= new_x < width and 0 <= new_y < height:
  #       new_img[new_x][new_y] = img[x,y]

    
  #       # new_img[new_x][new_y] = 255
  return bordes

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

    # bordesX[fila_actual] = min, max min<pixel<max
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
plt.show()

# cv2_imshow(mapeada)