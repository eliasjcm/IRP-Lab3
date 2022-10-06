import cv2
import numpy as np


def tiene_mapeo(a: complex, b: complex, c: complex, d: complex):
    print(f"{b}*{c}-{a}*{d}={b*c-a*d}")
    return b*c-a*d != complex(0, 0)


def crear_mapeo(a, b, c, d):
    return lambda z: (a*z + b) / (c*z + d)


def crear_mapeo_inverso(a, b, c, d):
    return lambda w: (-d*w + b) / (c*w - a)


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


def new_size(width, height, a, b, c, d):
    mapeo = crear_mapeo(a, b, c, d)
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


def generateImage(img, newImg, a, b, c, d):
    mapeo = crear_mapeo(a, b, c, d)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            z = mapeo(complex(x, y))
            new_x = int(z.real)
            new_y = int(z.imag)
            if 0 <= new_x < newImg.shape[0] and 0 <= new_y < newImg.shape[1]:
                newImg[new_x, new_y] = img[x, y]
    return newImg


def fillPixels(img, newImg, a, b, c, d):
    mapeo = crear_mapeo_inverso(a, b, c, d)
    for x in range(newImg.shape[0]):
        for y in range(newImg.shape[1]):
            if newImg[x, y] == 0:
                z = mapeo(complex(x, y))
                new_x = int(z.real)
                new_y = int(z.imag)
                if 0 <= new_x < img.shape[0] and 0 <= new_y < img.shape[1]:
                    newImg[x, y] = img[new_x, new_y]
    return newImg


def fillPixelsInterAux(img, newImg, a, b, c, d, inter8):
    mapeo = crear_mapeo_inverso(a, b, c, d)
    for x in range(newImg.shape[0]):
        for y in range(newImg.shape[1]):
            if newImg[x, y] == 0:
                z = mapeo(complex(x, y))
                new_x = int(z.real)
                new_y = int(z.imag)
                if 0 < new_x < img.shape[0]-1 and 0 < new_y < img.shape[1]-1:
                    if inter8:
                        newImg[x, y] = interpolacion8(img, new_x, new_y)
                    else:
                        newImg[x, y] = interpolacion4(img, new_x, new_y)
    return newImg


def newImage(img, a, b, c, d, should_fill=True):
    new_width, new_height = new_size(img.shape[0], img.shape[1], a, b, c, d)
    new_img = np.zeros((new_width, new_height), np.uint8)

    new_img = generateImage(img, new_img, a, b, c, d)
    if should_fill:
        new_img = fillPixels(img, new_img, a, b, c, d)
    return new_img


def newImageInterpolation4(img, a, b, c, d):
    new_width, new_height = new_size(img.shape[0], img.shape[1], a, b, c, d)
    new_img = np.zeros((new_width, new_height), np.uint8)

    new_img = generateImage(img, new_img, a, b, c, d)
    new_img = fillPixelsInterAux(img, new_img, a, b, c, d, False)
    return new_img


def newImageInterpolation8(img, a, b, c, d):
    new_width, new_height = new_size(img.shape[0], img.shape[1], a, b, c, d)
    new_img = np.zeros((new_width, new_height), np.uint8)

    new_img = generateImage(img, new_img, a, b, c, d)
    new_img = fillPixelsInterAux(img, new_img, a, b, c, d, True)
    return new_img


def addGaussianBlur(img, range):
    img = cv2.GaussianBlur(img, (range, range), 0)
    return img


if __name__ == "__main__":
    img = cv2.imread('ejemplo-original.png')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    primera = newImage(img_gray, 3 + 2.1j, 0, 0.004, 4+6j)
    cv2.imwrite("Punto_1-3.png", primera)
    print("✅ Imagen \"Punto 1-3.png\" creada")

    magnificacion = newImage(img_gray, 3, 0, 0, 1)
    cv2.imwrite("Punto_1-4-1.png", magnificacion)
    print("✅ Imagen \"Punto 1-4-1.png\" creada")

    magnificacion_rotacion = newImage(img_gray, 3, 0, 0, 1)
    cv2.imwrite("Punto_1-4-2.png", magnificacion_rotacion)
    print("✅ Imagen \"Punto 1-4-2.png\" creada")

    desplazamiento = newImage(img_gray, 1, 600+450j, 0, 1)
    cv2.imwrite("Punto_1-4-3.png", desplazamiento)
    print("✅ Imagen \"Punto 1-4-3.png\" creada")
    
    magnificacion_rotacion_desplazamiento = newImage(
        img_gray, 3+1j, 400+300j, 0, 1)
    cv2.imwrite("Punto_1-4-4.png", magnificacion_rotacion_desplazamiento)
    print("✅ Imagen \"Punto 1-4-4.png\" creada")

    imagen2 = newImage(img_gray, 2.1 + 2j, 0, 0.003, 1 + 1j, False)
    cv2.imwrite("imagen2.png", imagen2)
    print("✅ Imagen \"imagen2.png\" creada")

    imagen3 = newImage(img_gray, 2.1 + 2j, 0, 0.003, 1 + 1j, True)
    cv2.imwrite("imagen3.png", imagen3)
    print("✅ Imagen \"imagen3.png\" creada")

    imagen4 = newImageInterpolation4(img_gray, 2.1 + 2j, 0, 0.003, 1 + 1j)
    cv2.imwrite("imagen4.png", imagen4)
    print("✅ Imagen \"imagen4.png\" creada")

    imagen5 = newImageInterpolation8(img_gray, 2.1 + 2j, 0, 0.003, 1 + 1j)
    cv2.imwrite("imagen5.png", imagen5)
    print("✅ Imagen \"imagen5.png\" creada")

    imagen6 = addGaussianBlur(imagen2, 5)
    cv2.imwrite("imagen6.png", imagen6)
    print("✅ Imagen \"imagen6.png\" creada")

    imagen7 = addGaussianBlur(imagen4, 5)
    cv2.imwrite("imagen7.png", imagen7)
    print("✅ Imagen \"imagen7.png\" creada")

    imagen8 = addGaussianBlur(imagen5, 5)
    cv2.imwrite("imagen8.png", imagen8)
    print("✅ Imagen \"imagen8.png\" creada")
