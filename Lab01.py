import cv2

image = cv2.imread("lab1_imagen.png")
(height, width) = image.shape[:2]
image2 = image.copy()


def create_chess_pattern(img, color: list):
    """
    Función utilizada para crear el patrón de tablero de ajedrez coloreando la imagen con el color recibido.
    Los pixeles se pintan de forma que no hayan dos pixeles contiguos ni vertical ni horizontalmente pintados del mismo color recibido
    """
    height, width = img.shape[:2]
    for i in range(height):
        for j in range(width):
            # evita que dos pixeles contiguos sean pintados del mismo color
            if (i + j) % 2:
                img[i, j] = color

create_chess_pattern(image, [255,255,255])
create_chess_pattern(image2, [0, 0, 0])


cv2.imwrite("lab1_imagen1.png", image)
cv2.imwrite("lab1_imagen2.png", image2)