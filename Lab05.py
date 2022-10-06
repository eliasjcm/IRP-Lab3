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
    new_img = img.copy()
    height, width = img.shape[:2]
    picked_color = img[0][0]
    for x in range(height):
        for y in range(width):
            if (img[x][y] == picked_color).all():
                print(img[x][y])
                if not (x == 0 or x == (height-1) or y == 0 or y == (width-1)):
                    neighbours = np.array(
                        [img[x, y-1], img[x, y+1], img[x-1, y], img[x+1, y]])
                    new_img[x][y] = np.average(neighbours)
            else:
                new_img[x][y] = img[x][y]
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
    # img = cv2.imread('example.png')
    # img = convertGrayscale(img)
    # img = chessPixels(img, (0,0,0))
    # cv2.imwrite('chess.png', img)
    # # plt.imshow(img, cmap='gray')
    # # plt.show()
    # img = getPixelsInterpolation(img)
    # # plt.imshow(img, cmap='gray')
    # # plt.show()
    # highlightEdges(img, 'exampleLaplace.png', 3)
    # cv2.imwrite('example2.png', img)
    ddepth = cv2.CV_16S
    kernel_size = 3
    window_name = "Laplace Demo"
    # [variables]
    # [load]
    imageName = 'example.png'
    src = cv2.imread(cv2.samples.findFile(imageName),
                     cv2.IMREAD_COLOR)  # Load an image

    # Check if image is loaded fine
    if src is None:
        print('Error opening image')
        print('Program Arguments: [image_name -- default lena.jpg]')
        return -1
    # [load]
    # [reduce_noise]
    # Remove noise by blurring with a Gaussian filter
    src = chessPixels(src, (255, 255, 255))

    # src = cv2.GaussianBlur(src, (3, 3), 0)
    # src = cv2.resize(src, dsize=(src.shape[1], src.shape[0]), interpolation=cv2.INTER_CUBIC)
    src = getPixelsInterpolation(src)
    # [reduce_noise]
    # [convert_to_gray]
    # Convert the image to grayscale
    # src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # [convert_to_gray]
    # Create Window
    # cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    # [laplacian]
    # Apply Laplace function
    dst = cv2.Laplacian(src, ddepth, ksize=kernel_size)
    # [laplacian]
    # [convert]
    # converting back to uint8
    abs_dst = cv2.convertScaleAbs(dst)
    print(abs_dst)
    # [convert]
    # [display]
    final = cv2.add(src, abs_dst)
    cv2.imwrite('exampleLaplace_antes.png', src)
    cv2.imwrite('exampleLaplace_despues.png', final)
    # cv2.imshow(window_name, final)
    # cv2.waitKey(0)


main()
