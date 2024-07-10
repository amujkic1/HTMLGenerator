import cv2
import numpy as np
from flask import Flask, render_template, request, make_response
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
    draggable = request.cookies.get('draggable', 'false').lower() == 'true'

    if uploaded_file.filename != '':
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        contours = process_image_and_generate_html(image)
        html_output = generate_html_page(contours, button_color, image_width, image_height, bullet_style, font_family, draggable)
        return html_output
    else:
        return "No file uploaded."

@app.route("/enable_draggable", methods=["POST"])
def enable_draggable():
    response = make_response(f"Draggable enabled")
    response.set_cookie("draggable", "true")
    return response
@app.route("/disable_draggable", methods=["POST"])
def disable_draggable():
    response = make_response(f"Draggable disabled")
    response.set_cookie("draggable", "false")
    return response

@app.route("/get_draggable_state", methods=["GET"])
def get_draggable_state():
    draggable = request.cookies.get('draggable', 'false').lower()
    return draggable


if __name__ == "__main__":
    app.run()
