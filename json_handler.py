# json_handler.py

from flask import Blueprint, request, jsonify
import numpy as np
import tensorflow as tf

# Carrega o modelo pré-treinado
model = tf.keras.models.load_model("flaskr/model4.keras")

bp = Blueprint('json', __name__, url_prefix='/json')

maybeResults = ["bad_blue", "bad_red", "good_blue", "good_red"]

@bp.route('/', methods=['POST'])
def process_images():
    data = request.get_json()
    nImages = len(data['images'])
    wordResults = []

    for img_path in data['images']:
        img = img_path
        img_data = np.array([tf.keras.utils.load_img(img)])
        # Perform prediction using the loaded model
        wordResults.append(model.predict(img_data))

    results = ""
    for i in range(nImages):
        results += maybeResults[np.argmax(wordResults[i][0])]

    print(results)
    
    # Envia o comando ao Arduino
    if "good_blue" in results:
        print('A')  # Comando para "good_blue"
    elif "bad_blue" in results:
        print('B')  # Comando para "bad_blue"
    elif "good_red" in results:
        print('C')  # Comando para "good_red"
    elif "bad_red" in results:
        print('D')  # Comando para "bad_red"
    
    return jsonify(results)
