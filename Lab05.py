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
    picked_color = img[0][0]
    for x in range(height):
        for y in range(width):
            if (x + y) % 2 and not (x == 0 or x == (height-1) or y == 0 or y == (width-1)):
                neighbours = np.sum(
                    [img[x, y-1], img[x, y+1], img[x-1, y], img[x+1, y]], axis=0) / 4
                # print neighbours values

                # print(img[x, y-1], img[x, y+1], img[x-1, y],
                #       img[x+1, y], interpolation4(img,x,y), neighbours)
                new_img[x][y] = neighbours
                # print(np.average(neighbours))
    np.clip(new_img, 0, 255, out=new_img)
    # img[x, y] = interpolation4(img, x, y)
    return new_img


def highlightEdges(img, img_name, ksize):
    # laplaceMask = cv2.Laplacian(img, cv2.CV_64F, ksize=ksize)
    laplaceMask = cv2.Laplacian(img, cv2.CV_16S, ksize=ksize)
    # abs_dst = cv2.convertScaleAbs(laplaceMask)
    # laplaceMask = np.uint8(np.absolute(laplaceMask))

    plt.imshow(laplaceMask, cmap='gray')
    plt.show()
    cv2.imwrite(img_name, laplaceMask)

    height, width = img.shape[:2]

    for x in range(height):
        for y in range(width):
            img[x][y] = np.minimum(img[x][y] + laplaceMask[x][y], 255)

    plt.imshow(img, cmap='gray')
    plt.show()
    cv2.imwrite("exampleTest", img)


def main():
    ddepth = cv2.CV_16S
    kernel_size = 3
    imageName = '1.jpg'
    src = cv2.imread(cv2.samples.findFile(imageName),
                     cv2.IMREAD_COLOR)  # Load an image

    # Check if image is loaded fine
    if src is None:
        print('Error opening image')
        return -1

    create_chess_pattern(src, (0, 0, 0))

    src = getPixelsInterpolation(src)
    dst = cv2.Laplacian(src, ddepth, ksize=kernel_size)
    abs_dst = cv2.convertScaleAbs(dst)
    c = .2
    final = src + c * abs_dst
    cv2.imwrite('exampleLaplace_antes.png', src)
    cv2.imwrite('exampleLaplace_despues.png', final)


main()
