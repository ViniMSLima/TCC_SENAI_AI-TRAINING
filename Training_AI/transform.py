import os
import cv2 as cv
import numpy as np

def resize_and_process_image(image_path, output_dir, index, size=(128, 128)):
    img = cv.imread(image_path, cv.IMREAD_COLOR)

    if img is None:
        print(f"Erro ao ler a imagem: {image_path}")
        return

    # Aplica um filtro Gaussiano para suavizar a imagem
    img_blur = cv.GaussianBlur(img, (5, 5), 0)

    # Converte a imagem suavizada para HSV
    img_hsv = cv.cvtColor(img_blur, cv.COLOR_BGR2HSV)

    # Define a faixa de cor vermelha na escala HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv.inRange(img_hsv, lower_red, upper_red)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Aplica a máscara à imagem original para obter apenas as partes vermelhas
    img_red_filtered = cv.bitwise_and(img, img, mask=mask)

    # Converte a imagem para escala de cinza
    img_gray = cv.cvtColor(img_red_filtered, cv.COLOR_BGR2GRAY)

    # Binariza a imagem
    _, img_binary = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Redimensiona a imagem binarizada
    img_resized = cv.resize(img_binary, size)

    # Salva a imagem resultante em formato PNG
    output_path = os.path.join(output_dir, "0.png")
    cv.imwrite(output_path, img_resized, [cv.IMWRITE_PNG_COMPRESSION, 9])
    print(f"Imagem salva: {output_path}")

def process_images_from_directory(directory, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_index = 0

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                img_path = os.path.join(subdir, file)
                resize_and_process_image(img_path, output_dir, image_index)
                image_index += 1

print("transforming")
directory = 'processed_images'
output_directory = 'AI/datasets/OUT/images/good'
input_dir = os.path.join(directory, "test")
process_images_from_directory(input_dir, output_directory)
