# Lab 3
# Elaborado por:
#   - Elías Josué Castro Montero - 2020098930
#   - Abiel Porras Garro - 2020209597

import cv2
import numpy as np

def edge_detection(img_name):
    img = cv2.imread(img_name)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height, width = img_gray.shape[:2]
    # Arrays de zeros del mismo tamaño que la imagen
    # borders_x almacena los valores utilizando la derivada en x
    # borders_y almacena los valores utilizando la derivada en y
    borders_x = np.zeros((height, width), np.uint8)
    borders_y = np.zeros((height, width), np.uint8)

    # Aplicamos la derivada en x
    for x in range(width - 1):
        for y in range(height - 1):
            # Nos interesa la diferencia entre el pixel actual y el siguiente (derecha)
            derivative_x = abs(int(img_gray[y, x]) - int(img_gray[y, x+1]))
            borders_x[y, x] = derivative_x

    # Aplicamos la derivada en y
    for x in range(width - 1):
        for y in range(height - 1):
            # Nos interesa la diferencia entre el pixel actual y el siguiente (abajo)
            derivative_y = abs(int(img_gray[y, x]) - int(img_gray[y+1, x]))
            borders_y[y, x] = derivative_y

    # Sumamos los valores de las derivadas en x e y
    # Estos valores deben limitarse a 255 para que no se desborde
    image_borders = np.minimum(borders_x + borders_y, 255)

    cv2.imwrite("bordesX.jpg", borders_x)
    print("✅ Bordes en eje X guardados en 'bordesX.jpg'")
    cv2.imwrite("bordesY.jpg", borders_y)
    print("✅ Bordes en eje Y guardados en 'bordesY.jpg'")
    cv2.imwrite("bordes.jpg", image_borders)
    print("✅ Bordes superpuestos (eje X y Y) guardados en 'bordes.jpg'")


if __name__ == "__main__":
    image_name = input("Ingrese el nombre de la imagen: ")
    edge_detection(image_name)
