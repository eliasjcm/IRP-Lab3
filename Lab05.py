import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def convertGrayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def interpolation4(img, x, y):
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


def create_chess_pattern(img, color: list) -> np.ndarray:
    """
    Función utilizada para crear el patrón de tablero de ajedrez coloreando la imagen con el color recibido.
    Los pixeles se pintan de forma que no hayan dos pixeles contiguos ni vertical ni horizontalmente pintados del mismo color recobido
    """
    height, width = img.shape[:2]
    for i in range(height):
        for j in range(width):
            # evita que dos pixeles contiguos sean pintados del mismo color
            if (i + j) % 2:
                img[i, j] = color


def getPixelsInterpolation(img):
    new_img = img.copy()
    height, width = img.shape[:2]
    for x in range(height):
        for y in range(width):
            if (x + y) % 2 and not (x == 0 or x == (height-1) or y == 0 or y == (width-1)):
                neighbours = np.sum(
                    [img[x, y-1], img[x, y+1], img[x-1, y], img[x+1, y]], axis=0) / 4
                new_img[x][y] = neighbours
            else:
                new_img[x][y] = img[x][y]

    np.clip(new_img, 0, 255, out=new_img)
    return new_img


def retrieve_image_info(img_name):
    img = cv2.imread(cv2.samples.findFile(img_name),
                     cv2.IMREAD_COLOR)  # Load an image

    # Check if image is loaded fine
    if img is None:
        print('Error opening image')
        return -1
    return getPixelsInterpolation(img)


def improve_sharpness(img, c):
    ddepth = cv2.CV_16S
    kernel_size = 3
    dst = cv2.Laplacian(img, ddepth, ksize=kernel_size)
    abs_dst = cv2.convertScaleAbs(dst)
    final = img + c * abs_dst
    return final


def main():

    lab5_imagen1 = retrieve_image_info("lab1_imagen1.png")
    lab5_imagen2 = retrieve_image_info("lab1_imagen2.png")

    cv2.imwrite("lab5_imagen1.png", lab5_imagen1)
    cv2.imwrite("lab5_imagen2.png", lab5_imagen2)

    lab5_imagen3 = improve_sharpness(lab5_imagen1, -0.2)
    lab5_imagen4 = improve_sharpness(lab5_imagen2, -0.2)

    cv2.imwrite("lab5_imagen3", lab5_imagen3)
    cv2.imwrite("lab5_imagen4.png", lab5_imagen4)


main()
