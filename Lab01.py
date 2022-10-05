import cv2

image = cv2.imread("lab1_imagen.jpg")
(height, width) = image.shape[:2]
image2 = image.copy()

for y in range(height):
    if y % 2 == 0:
        for x in range(width):
            if x % 2 == 0:
                image[y][x] = [0, 0, 0]
    else:
        for x in range(width):
            if x % 2 != 0:
                image[y][x] = [0, 0, 0]

for y in range(height):
    if y % 2 == 0:
        for x in range(width):
            if x % 2 == 0:
                image2[y][x] = [255, 255, 255]
    else:
        for x in range(width):
            if x % 2 != 0:
                image2[y][x] = [255, 255, 255]

cv2.imwrite("lab1_imagen2.jpg", image)
cv2.imwrite("lab1_imagen1.jpg", image2)