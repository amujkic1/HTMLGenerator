import cv2
import numpy as np
from flask import Flask, render_template, request
from process_image import process_image_and_generate_html
from generate_html import generate_html_page

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_html", methods=["POST"])
def generate_html_route():
    uploaded_file = request.files['file']
    button_color = request.form.get('buttonColor')
    image_width = int(request.form.get('imageWidth'))
    image_height = int(request.form.get('imageHeight'))
    bullet_style = request.form.get('bulletStyle')
    font_family = request.form.get('fontFamily')
    if uploaded_file.filename != '':
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        contours = process_image_and_generate_html(image)
        html_output = generate_html_page(contours, button_color, image_width, image_height, bullet_style, font_family)
        return html_output
    else:
        return "No file uploaded."



if __name__ == "__main__":
    app.run()
