import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
# from skimage import io
# from google.colab.patches import cv2_imshow

img = cv2.imread('lenna.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# def crearImagenLlenaColorSolido(bordes, pixeles):
#   new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
#   for p in pixeles:
#     new_img[p[0], p[1]] = 255

#   for x in range(bordes[0][0]):
#     for y in range(bordes[0][1]):
#       if new_img[x, y] == 0:
#         if x in bordes[1]:
#           if bordes[1][x][0] <= y <= bordes[1][x][1]:
#             new_img[x, y] = 255
#         if y in bordes[2]:
#           if bordes[2][y][0] <= x <= bordes[2][y][1]:
#             new_img[x, y] = 255
#   return new_img

# def bordesC(img, a, b, c, d):
#   mapeo = crear_mapeo(a, b, c, d)
#   width, height = img.shape
#   print(img.shape)
#   bordes = [[0, 0], {}, {}]
#   pixeles = []
#   print(bordes)
#   # new_img = np.zeros((width, height), np.uint8)

#   for x in range(width):
#     for y in range(height):
#       w = mapeo(complex(x, y))
#       # if ()
#       new_x = int(w.real)
#       new_y = int(w.imag)
#       # print(new_x, new_y)
#       pixeles.append([new_x, new_y, img[x,y]])
      
#       if new_x not in bordes[1]:
#         bordes[1][new_x] = [new_y, new_y]
#       else:
#         if new_y < bordes[1][new_x][0]:
#           bordes[1][new_x][0] = new_y
#         elif new_y > bordes[1][new_x][1]:
#           bordes[1][new_x][1] = new_y

#       if new_y not in bordes[2]:
#         bordes[2][new_y] = [new_x, new_x]
#       else:
#         if new_x < bordes[2][new_y][0]:
#           bordes[2][new_y][0] = new_x
#         elif new_x > bordes[2][new_y][1]:
#           bordes[2][new_y][1] = new_x

#       bordes[0][0] = max(bordes[0][0], new_x)
#       bordes[0][1] = max(bordes[0][1], new_y)

#   print(bordes[0])

#   bordes[0][0] += 1
#   bordes[0][1] += 1
    
#   print(bordes[0])

#   return bordes, pixeles

def tiene_mapeo(a: complex, b: complex, c: complex, d: complex):
  print(f"{b}*{c}-{a}*{d}={b*c-a*d}")
  return b*c-a*d != complex(0,0)
  
def crear_mapeo(a, b, c, d):
  return lambda z : (a*z + b) / (c*z + d)

def crear_mapeo_inverso(a, b, c, d):
  return lambda w : (-d*w + b) / (c*w - a)

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

def crearNuevaImagen(img, a, b, c, d):
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


def crearImagenLlenaInter(img, mapeo, bordes, pixeles):

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
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    new_img[p[0], p[1]] = p[2]

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
          if x in bordes[1] or y in bordes[2]:
            if (bordes[1][x][0] <= y <= bordes[1][x][1]) or (bordes[2][y][0] <= x <= bordes[2][y][1]):
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              if not (new_x == 0 or new_x == (img.shape[0]-1) or new_y == 0 or new_y == (img.shape[0]-1)):
                if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
                  new_img[x, y] = interpolacion8(img, new_x, new_y) 
            else:
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              if not (new_x == 0 or new_x == (img.shape[0]-1) or new_y == 0 or new_y == (img.shape[0]-1)):
                if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
                  new_img[x, y] = interpolacion8(img, new_x, new_y) 
  return new_img

def mapear_imagen(img, a, b, c, d):
  mapeo = crear_mapeo(a, b, c, d)
  mapeo_inverso = crear_mapeo_inverso(a, b, c, d)
  width, height = img.shape
  print(img.shape)
  new_img = np.zeros((width, height), np.uint8)
  for x in [0, width-1]:
    for y in range(height):
      w = mapeo(complex(x, y))
      # if ()
      new_x = int(w.real)
      new_y = int(w.imag)
      # print(new_x, new_y)
      if 0 <= new_x < width and 0 <= new_y < height:
        new_img[new_x][new_y] = img[x,y]

  for y in [0, height-1]:
    for x in range(width):
      w = mapeo(complex(x, y))
      # if ()
      new_x = int(w.real)
      new_y = int(w.imag)
      # print(new_x, new_y)
      if 0 <= new_x < width and 0 <= new_y < height:
        new_img[new_x][new_y] = img[x,y]
  return new_img

def crearImagen(bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    new_img[p[0], p[1]] = 255
  return new_img

def crearImagenLlena(img, mapeo, bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    new_img[p[0], p[1]] = p[2]

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
        if x in bordes[1] or y in bordes[2]:
          if (bordes[1][x][0] < y < bordes[1][x][1]) or (bordes[2][y][0] < x < bordes[2][y][1]):
            z = mapeo(complex(x, y))
            new_x = int(z.real)
            new_y = int(z.imag)
            if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
              new_img[x, y] = img[new_x, new_y]  
          else:
            z = mapeo(complex(x, y))
            new_x = int(z.real)
            new_y = int(z.imag)
            # print("Forma2", x, y, new_x, new_y)
            if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
              new_img[x, y] = img[new_x, new_y]   
  return new_img

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

def crearImagenLlenaInter(img, mapeo, bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    new_img[p[0], p[1]] = p[2]

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
          if x in bordes[1] or y in bordes[2]:
            if (bordes[1][x][0] <= y <= bordes[1][x][1]) or (bordes[2][y][0] <= x <= bordes[2][y][1]):
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              if not (new_x == 0 or new_x == (img.shape[0]-1) or new_y == 0 or new_y == (img.shape[0]-1)):
                if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
                  new_img[x, y] = interpolacion8(img, new_x, new_y) 
            else:
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              if not (new_x == 0 or new_x == (img.shape[0]-1) or new_y == 0 or new_y == (img.shape[0]-1)):
                if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
                  new_img[x, y] = interpolacion8(img, new_x, new_y) 
  return new_img


# bordes, pixels = bordesC(img_gray, 2.1+2.1j, 1, 0.003, 1+1j)
# mapeo = crear_mapeo_inverso(2.1+2.1j, 1, 0.003, 1+1j)
# new_img = crearImagenLlena(img_gray, mapeo, bordes, pixels)

# bordes, pixels = bordesC(img_gray, 6, 0, 0, 1)
# mapeo = crear_mapeo_inverso(6, 0, 0, 1)
# new_img = crearImagenLlena(img_gray, mapeo, bordes, pixels)
# print("Magnificación: magnificacion.png")
# cv2.imwrite("magnificacion.png", new_img)

new_img = crearNuevaImagen(img_gray, 6, 0, 0, 1)

# new_img = mapear_imagen(img_gray, 2.1+2.1j, 0, 0.003, 1+1j)


# blur = cv2.GaussianBlur(new_img,(5,5),0)

# m1 = mapeo(complex(36, 380))
# x1 = int(m1.real)
# y1 = int(m1.imag)
# print("1,1:", x1, y1)
# m2 = mapeo(complex(0, 1))
# x2 = int(m2.real)
# y2 = int(m2.imag)
# print("0,1:", x2, y2)


plt.imshow(new_img)
plt.show()

cv2.imwrite("Test.png", new_img)

# cv2_imshow(mapeada)