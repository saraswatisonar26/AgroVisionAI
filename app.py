import os
import numpy as np
import tensorflow as tf
from disease_info import DISEASE_INFO
from PIL import Image

from class_names import CLASS_NAMES

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request

app = Flask(__name__)
MODEL_PATH = "model/best_model.keras"

model = tf.keras.models.load_model(MODEL_PATH)
UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect")
def detect():
    return render_template("detect.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/predict", methods=["POST"])
def predict():

    image = request.files["image"]

    if image.filename == "":
        return "No Image Selected"

    filename = secure_filename(image.filename)

    image_path = os.path.join(UPLOAD_FOLDER, filename)

    image.save(image_path)

    # ---------- Image Preprocessing ----------

    img = Image.open(image_path).convert("RGB")

    img = img.resize((224, 224))

    img_array = np.array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    # ---------- Prediction ----------

    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction)

    confidence = np.max(prediction) * 100

    disease_name = CLASS_NAMES[predicted_class]
    info = DISEASE_INFO.get(
    disease_name,
    {
        "symptoms": ["Information not available"],
        "treatment": ["Information not available"],
        "prevention": ["Information not available"]
    }
)

    return render_template(

    "result.html",

    uploaded_image="uploads/" + filename,

    disease=disease_name,

    confidence=round(confidence,2),

    info=info

)




    


if __name__ == "__main__":
    app.run(debug=True)