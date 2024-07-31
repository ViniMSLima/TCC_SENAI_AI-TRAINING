import numpy as np
import tensorflow as tf
import sys

# Load the pre-trained model
model = tf.keras.models.load_model("checkpoints/model4.keras")

maybeResults = ["bad_blue", "bad_red", "good_blue", "good_red", "good_white"]

def main():
    nImages = 6
    
    wordResults = []
    
    for i in range(nImages):    
        img = "testing_dataset/" + str(i) + ".png"
        data = np.array([tf.keras.utils.load_img(img)])
           
        # Perform prediction using the loaded model
        wordResults.append(model.predict(data))
    
    a = ""    
    for i in range(nImages):
        a += f"{maybeResults[np.argmax(wordResults[i][0])]}\n"
    
    # Write the result to stdout

    sys.stdout.write(a)
    sys.stdout.flush()

if __name__ == "__main__":
    main()