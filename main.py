import os
import cv2
import numpy as np


def edge_detection(img_path):
    print(img_path)
    # img = cv2.imread("edificio_con_arboles.jpg")
    # img_path = input("Ingrese la ruta de la imagen: ")
    img = cv2.imread(img_path)
    # img = cv2.imread("popular.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite("gray.jpg", img_color)

    height, width = img_gray.shape[:2]
    print(f"height: {height}, width: {width}")
    new_image = np.zeros((height, width), np.uint8)

    for x in range(width - 1):
        for y in range(height - 1):
            derivative_x = abs(int(img_gray[y, x]) - int(img_gray[y, x+1]))
            new_image[y, x] = derivative_x
            derivative_y = abs(int(img_gray[y, x]) - int(img_gray[y+1, x]))
            new_image[y, x] = min((new_image[y, x] + derivative_y), 255)

    cv2.imwrite(f"../bordes/BORDES-{img_path}", new_image)
    # print(new_image[0, :])


os.chdir("./discord-imagenes")
for img in os.listdir():
    edge_detection(img)