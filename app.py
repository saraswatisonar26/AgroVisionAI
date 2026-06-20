import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request

app = Flask(__name__)

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

    upload_folder = os.path.join(app.static_folder, "uploads")

    os.makedirs(upload_folder, exist_ok=True)

    image.save(os.path.join(upload_folder, filename))

    image_path = "uploads/" + filename

    return render_template(
        "result.html",
        uploaded_image=image_path
    )
    


if __name__ == "__main__":
    app.run(debug=True)