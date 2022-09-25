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
  return lambda w : (-d*w + b) / (c*w - a)

def bordes(img, a, b, c, d):
  mapeo = crear_mapeo(a, b, c, d)
  width, height = img.shape
  print(img.shape)
  bordes = [[0, 0], {}, {}]
  print(bordes)
  # new_img = np.zeros((width, height), np.uint8)
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

      bordes[0][0] = max(bordes[0][0], new_x)
      bordes[0][1] = max(bordes[0][1], new_y)

  for x in [0, width-1]:
    for y in range(height):
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

      bordes[0][0] = max(bordes[0][0], new_x)
      bordes[0][1] = max(bordes[0][1], new_y)

    
  print(bordes[0])
  print(bordes[1])
  print("\n\n\n")
  print(bordes[2])

  return bordes

def bordesC(img, a, b, c, d):
  mapeo = crear_mapeo(a, b, c, d)
  width, height = img.shape
  print(img.shape)
  bordes = [[0, 0], {}, {}]
  pixeles = []
  print(bordes)
  # new_img = np.zeros((width, height), np.uint8)

  for x in range(width):
    for y in range(height):
      w = mapeo(complex(x, y))
      # if ()
      new_x = int(w.real)
      new_y = int(w.imag)
      # print(new_x, new_y)
      pixeles.append([new_x, new_y])

      if new_x not in bordes[1]:
        bordes[1][new_x] = [new_y, new_y]
      else:
        if new_y < bordes[1][new_x][0]:
          bordes[1][new_x][0] = new_y
        elif new_y > bordes[1][new_x][1]:
          bordes[1][new_x][1] = new_y

      if new_y not in bordes[2]:
        bordes[2][new_y] = [new_x, new_x]
      else:
        if new_x < bordes[2][new_y][0]:
          bordes[2][new_y][0] = new_x
        elif new_x > bordes[2][new_y][1]:
          bordes[2][new_y][1] = new_x

      bordes[0][0] = max(bordes[0][0], new_x)
      bordes[0][1] = max(bordes[0][1], new_y)

  bordes[0][0] += 1
  bordes[0][1] += 1
    
  print(bordes[0])
  print(bordes[1])
  print("\n\n\n")
  print(bordes[2])
  print("\n\n\n")
  # print(pixeles)

  return bordes, pixeles

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

def crearImagenLlenaColorSolido(bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    new_img[p[0], p[1]] = 255

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
        if x in bordes[1]:
          if bordes[1][x][0] <= y <= bordes[1][x][1]:
            new_img[x, y] = 255
        if y in bordes[2]:
          if bordes[2][y][0] <= x <= bordes[2][y][1]:
            new_img[x, y] = 255
  return new_img

def crearImagenLlena(img, mapeo, bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    z = mapeo(complex(p[0], p[1]))
    new_x = int(z.real)
    new_y = int(z.imag)
    new_img[p[0], p[1]] = img[new_x, new_y]

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
        if x in bordes[1]:
          if bordes[1][x][0] <= y <= bordes[1][x][1]:
            z = mapeo(complex(x, y))
            new_x = int(z.real)
            new_y = int(z.imag)
            new_img[x, y] = img[new_x, new_y]
        if y in bordes[2]:
          if bordes[2][y][0] <= x <= bordes[2][y][1]:
            z = mapeo(complex(x, y))
            new_x = int(z.real)
            new_y = int(z.imag)
            new_img[x, y] = img[new_x, new_y]
  return new_img

def interpolacion4(img, x, y):
  # print(x, y , x-1 , y-1, x+1, y+1)
  # print(img[x, y-1], img[x, y+1], img[x-1, y], img[x+1, y])
  count = 0
  value = img[x, y-1]
  count += value
  # print(f"val1 {count}")
  value = img[x, y+1]
  count += value
  # print(f"val2 {count}")
  value = img[x-1, y]
  count += value
  # print(f"val3 {count}")
  value = img[x+1, y]
  count += value
  # print(f"val4 {count}")
  count = count / 4
  # print(f"val5 {count}")
  return count

def interpolacion8(img, x, y):
  # print(x, y , x-1 , y-1, x+1, y+1)
  # print(img[x, y-1], img[x, y+1], img[x-1, y], img[x+1, y], "ff", img[x-1, y-1], img[x+1, y-1], img[x-1, y+1], img[x+1, y+1])
  count = 0
  value = img[x, y-1]
  count += value
  # print(f"val1 {count}")
  value = img[x, y+1]
  count += value
  # print(f"val2 {count}")
  value = img[x-1, y]
  count += value
  # print(f"val3 {count}")
  value = img[x+1, y]
  count += value
  # print(f"val4 {count}")
  value = img[x-1, y-1]
  count += value
  # print(f"val5 {count}")
  value = img[x-1, y+1]
  count += value
  # print(f"val6 {count}")
  value = img[x+1, y-1]
  count += value
  # print(f"val7 {count}")
  value = img[x+1, y+1]
  count += value
  # print(f"val8 {count}")
  count = count / 8
  # print(f"val9 {count}")
  return count

def crearImagenLlenaInter(img, mapeo, bordes, pixeles):
  new_img = np.zeros((bordes[0][0], bordes[0][1]), np.uint8)
  for p in pixeles:
    z = mapeo(complex(p[0], p[1]))
    new_x = int(z.real)
    new_y = int(z.imag)
    new_img[p[0], p[1]] = img[new_x, new_y]

  for x in range(bordes[0][0]):
    for y in range(bordes[0][1]):
      if new_img[x, y] == 0:
        # print(x, y)
        if not (x == 0 or x == bordes[0][0] or y == 0 or y == bordes[0][1]):
          if x in bordes[1]:
            if bordes[1][x][0] <= y <= bordes[1][x][1]:
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              new_img[x, y] = interpolacion4(img, new_x, new_y)
          if y in bordes[2]:
            if bordes[2][y][0] <= x <= bordes[2][y][1]:
              z = mapeo(complex(x, y))
              new_x = int(z.real)
              new_y = int(z.imag)
              new_img[x, y] = interpolacion4(img, new_x, new_y)
  return new_img


bordes, pixels = bordesC(img_gray, 2.1+2.1j, 0, 0.003, 1+1j)
mapeo = crear_mapeo_inverso(2.1+2.1j, 0, 0.003, 1+1j)
new_img = crearImagenLlena(img_gray, mapeo, bordes, pixels)


blur = cv2.GaussianBlur(new_img,(5,5),0)


plt.imshow(blur)
plt.show()

cv2.imwrite("BuscandoPixelGaussiano.png", blur)

# cv2_imshow(mapeada)