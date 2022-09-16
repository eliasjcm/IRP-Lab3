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
    # new_image = np.zeros(img.shape)
    # x_image = np.zeros((height, width), np.uint8)
    # y_image = np.zeros((height, width), np.uint8)

    # #set a thresh
    # thresh = 100
    # #get threshold image
    # ret,thresh_img = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)
    # #find contours
    # contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # # draw the contours on the empty image
    # cv2.drawContours(new_image, contours, -1, (255,255,255), 1)

    t_lower = 50  # Lower Threshold
    t_upper = 150  # Upper threshold
  
    # Applying the Canny Edge filter
    new_image = cv2.Canny(img_gray, t_lower, t_upper)

    cv2.imwrite(f"../bordes/BORDES-{img_path}", new_image)
    # print(new_image[0, :])


os.chdir("./discord-imagenes")
for img in os.listdir():
    edge_detection(img)
