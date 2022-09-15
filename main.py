import cv2
import matplotlib.pyplot as plt
import numpy as np

# img = cv2.imread("edificio_con_arboles.jpg")
img = cv2.imread("el-paisaje-urbano-europeo-combinado-con-la-naturaleza-berna-es-una-inusual-capital-europea-su-perfecta-mezcla-rADo-aare-da-otra-164795497.jpg")
# img = cv2.imread("popular.jpg")
img_color = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imwrite("gray.jpg", img_color)

height, width = img_color.shape[:2]
new_image = np.zeros((height, width), np.uint8)


for y in range(height):
    for x in range(width):
        if x - 1 >= 0:
            derivative = abs(int(img_color[y, x]) - int(img_color[y, x-1]))
            new_image[y, x] = derivative
        if y - 1 >= 0:
            derivative = abs(int(img_color[y, x]) - int(img_color[y-1, x]))
            new_image[y, x] = (new_image[y, x] + derivative) % 256


cv2.imwrite("new_image_2.jpg", new_image)
# plt.imshow(img_color)