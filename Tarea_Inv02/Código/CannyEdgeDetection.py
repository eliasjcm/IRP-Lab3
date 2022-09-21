# Detector de bordes utilizando Canny Edge Detection
# Elaborado por:
#   - Elías Josué Castro Montero - 2020098930
#   - Abiel Porras Garro - 2020209597

import cv2
import os


def canny(img_name):
    img = cv2.imread(img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Busca los bordes utilizando Canny Edge Detection con los valores de threshold entre 30 y 200
    edged = cv2.Canny(gray, 30, 200)

    cv2.imwrite(f"../bordes-canny-edge-detection/bordes-{img_name}", edged)


if __name__ == "__main__":
    os.chdir("./discord-imagenes")
    # creamos el directorio para guardar las imágenes de bordes si no existe
    if not os.path.exists("../bordes-canny-edge-detection"):
        os.mkdir("../bordes-canny-edge-detection")
    for img in os.listdir():
        canny(img)
    print("✅ Bordes correctamente generados")
