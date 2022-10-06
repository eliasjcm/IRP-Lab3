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

def chessPixels(img, color):
    height, width = img.shape[:2]
    for y in range(height):
        if y % 2 == 0:
            for x in range(width):
                if x % 2 == 0:
                    img[y][x] = color
        else:
            for x in range(width):
                if x % 2 != 0:
                    img[y][x] = color
    return img

def getPixelsInterpolation(img):
    height, width = img.shape[:2]

    for x in range(height):
        for y in range(width):
            if img[x][y] == 0 or img[x][y] == 255:
                if not (x == 0 or x == (height-1) or y == 0 or y == (width-1)):
                    img[x, y] = interpolation4(img, x, y)
    return img

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
    img = cv2.imread('example.png')
    img = convertGrayscale(img)
    img = chessPixels(img, 0)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    img = getPixelsInterpolation(img)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    highlightEdges(img, 'exampleLaplace.png', 3)
    cv2.imwrite('example2.png', img)

main()