import cv2
import matplotlib.pyplot as plt
import numpy as np


# img = cv2.imread("./000-32jd6nd_2444344_20220914100524.jpg")
# img = cv2.imread("edificio_con_arboles.jpg")
img = cv2.imread("el-paisaje-urbano-europeo-combinado-con-la-naturaleza-berna-es-una-inusual-capital-europea-su-perfecta-mezcla-rADo-aare-da-otra-164795497.jpg")
img_color = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imwrite("gray.jpg", img_color)

height, width = img_color.shape[:2]
new_image = np.zeros((height, width), np.uint8)


for y in range(height):
    for x in range(width):
        if not x - 1 < 0:
            derivative = abs(int(img_color[y, x]) - int(img_color[y, x-1]))
            if derivative < 5:
                new_image[y, x] = 128
            else:
                new_image[y, x] = 0
        else:
            new_image[y, x] = 0

# iterate columns of the image
for y in range(height):
    for x in range(width):
        if not y - 1 < 0:
            derivative = abs(int(img_color[y, x]) - int(img_color[y-1, x]))
            if derivative < 5:
                new_image[y, x] = (new_image[y, x] + 128) % 256


cv2.imwrite("new_image.jpg", new_image)
# plt.imshow(img_color)