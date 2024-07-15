import serial
import time
from flask import Blueprint, request, jsonify
import numpy as np
import tensorflow as tf

# Configura a porta serial e a taxa de baud
ser = serial.Serial('/dev/cu.usbserial-14330', 9600)
time.sleep(2)  # Aguarda a inicialização da comunicação serial

def send_command(command):
    ser.write(command.encode())

# Carrega o modelo pré-treinado
model = tf.keras.models.load_model("flaskr/model5.keras")

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
        send_command('A')  # Comando para "good_blue"
    elif "bad_blue" in results:
        send_command('B')  # Comando para "bad_blue"
    elif "good_red" in results:
        send_command('C')  # Comando para "good_red"
    elif "bad_red" in results:
        send_command('D')  # Comando para "bad_red"
    
    return jsonify(results)

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(debug=True)
