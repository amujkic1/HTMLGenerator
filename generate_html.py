import cv2

def generate_html_page(contours, button_color, image_width, image_height, bullet_style, font_family):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contour Analysis</title>
        <style>
            .draggable {
                position: absolute;
                cursor: grab;
            }
        </style>
    </head>
    <body>
    """

    num = 0
    x_current = 0
    y_current = 0
    EPSILON_X = 100
    EPSILON_Y = 20

    contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[0])

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x_new, y_new, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)
        x_tmp = x_new
        y_tmp = y_new

        num += 1
        print(num)

        # Alignment
        # Check if this is the first contour
        if x_current == 0 and y_current == 0:
            x_current = x_new
            y_current = y_new
        else:
            if abs(x_new - x_current) < EPSILON_X:
                x_new = x_current
            if abs(y_new - y_current) < EPSILON_Y:
                y_new = y_current

        print('trenutno ', x_current, ' ', y_current)
        print('novo ', x_new, ' ', y_new)

        if num_vertices >= 3 and area > 100:
            # Button
            if area < 5000 and num_vertices < 7:
                html += f'<button id="btn{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px; background-color: {button_color};">Click Me</button>'
            # Text paragraph
            elif area < 5000 and num_vertices >= 7:
                html += f'<p id="txt{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px; font-size: 18px; font-family: {font_family};">Some Text</p>'
            # Input field
            elif area > 5000 and h / w < 0.5:
                html += f'<input id="input{idx}" class="draggable" type="text" style="left: {x_new}px; top: {y_new}px; width: {w}px; height: {h}px;">'
            # Image
            else:
                for child_contour in contours:
                    if len(cv2.approxPolyDP(child_contour, 0.04 * cv2.arcLength(child_contour, True), True)) >= 3:
                        html += f'<img id="img{idx}" class="draggable" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="Custom Shape" style="left: {x_new}px; top: {y_new}px; width: {image_width}px; height: {image_height}px;">'
                        break
        elif num_vertices == 2 and area > 100:
            html += f'<ul id="txt{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px; font-size: 18px; list-style-type: {bullet_style}; font-family: {font_family};">'
            html += '<li>List item</li>'
            html += '</ul>'

    html += """
        <script>
            const draggableElements = document.querySelectorAll('.draggable');
            let offsetX, offsetY, isDragging = false, activeElement;

            draggableElements.forEach(element => {
                element.addEventListener('mousedown', (event) => {
                    isDragging = true;
                    activeElement = element;
                    offsetX = event.clientX - element.getBoundingClientRect().left;
                    offsetY = event.clientY - element.getBoundingClientRect().top;
                    element.style.cursor = 'grabbing';
                });
            });

            document.addEventListener('mousemove', (event) => {
                if (isDragging) {
                    const x = event.clientX - offsetX;
                    const y = event.clientY - offsetY;
                    activeElement.style.left = `${x}px`;
                    activeElement.style.top = `${y}px`;
                }
            });

            document.addEventListener('mouseup', () => {
                isDragging = false;
                if (activeElement) {
                    activeElement.style.cursor = 'grab';
                    activeElement = null;
                }
            });
        </script>
    </body>
    </html>
    """
    return html
