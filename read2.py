import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('C:\\Users\\HP\\Desktop\\probni_set\\dipl1.jpg')

# Resize the image
desired_width = 1000
desired_height = 700
scaled_image = cv2.resize(image, (desired_width, desired_height))

# Convert the image to grayscale
gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_BGR2RGB))
plt.title('Grayscale')
plt.show()

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Find edges using Canny edge detection
edged = cv2.Canny(blurred_image, 30, 200)

# Find contours and hierarchy
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours (noise)
min_contour_area = 1  # Adjust this threshold as needed
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Draw contours on the original image
contour_image = scaled_image.copy()
cv2.drawContours(contour_image, filtered_contours, -1, (0, 255, 0), 1)

# Display the results
plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
plt.title('Contours')
plt.show()

print("Number of Contours found = " + str(len(filtered_contours)))

# Iterate through contours and hierarchy
for idx, (contour, hier) in enumerate(zip(filtered_contours, hierarchy[0])):
    # Check if contour has child
    if hier[2] != -1:
        child_contour = contours[hier[2]]
        # Calculate distance between contour and its child
        distance = cv2.matchShapes(contour, child_contour, cv2.CONTOURS_MATCH_I2, 0.0)
        print(f"Contour {idx + 1} has child with distance {distance:.2f}")
    else:
        print(f"Contour {idx + 1} has no child")

def analyze_contours_and_generate_html(contours):
    num = 0
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    html = ""

    # Sort the contours by the top-left corner coordinates
    sorted_contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[0])

    for idx, contour in enumerate(sorted_contours):
        # Calculate contour properties
        num += 1
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)

        # Calculate percentage of area occupied by current contour
        area_percentage = (area / total_area) * 100

        # Generate HTML based on contour properties, including width and height
        html += f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; border: 2px solid red;">'
        #html += f'Top-left : ({x}, {y})<br>'  # Add top-left coordinates
        html += f'Area: {area} (Percentage: {area_percentage:.2f}% of total)<br>'
        #html += f'Ratio: {h/w}<br>'
        #html += f'Number of Vertices: {num_vertices}<br>'
        #html += f'Contour no. {num}'
        html += '</div><br>'

    return html

    return html


# Generate HTML based on contour shapes
html_output = analyze_contours_and_generate_html(contours)

# Save the HTML to a file or display it
with open('output5.html', 'w') as f:
    f.write(html_output)

def generate_html_page(contours):
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

    x_current = 0
    y_current = 0
    EPSILON = 100
    for idx, contour in enumerate(contours):
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x_new, y_new, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)

        if num_vertices >= 3 and area > 100:
            # Button
            if area < 5000 and num_vertices < 7:
                html += f'<button id="btn{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px;">Click Me</button>'
            elif area < 5000 and num_vertices >= 7:
                html += f'<p id="txt{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px; font-size: 18px;">Some Text</p>'
            elif area > 5000 and h / w < 0.5:
                html += f'<input id="input{idx}" class="draggable" type="text" style="left: {x_new}px; top: {y_new}px; width: {w}px; height: {h}px;">'
            else:
                for child_contour in contours:
                    if len(cv2.approxPolyDP(child_contour, 0.04 * cv2.arcLength(child_contour, True), True)) >= 3:
                        # Draw an image at the location of the parent contour
                        html += f'<img id="img{idx}" class="draggable" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="Custom Shape" style="left: {x_new}px; top: {y_new}px; width: {w}px; height: {h}px;">'
                        break  # Break the loop after drawing one image
        elif num_vertices == 2 and area > 100:
            html += f'<ul id="txt{idx}" class="draggable" style="left: {x_new}px; top: {y_new}px; font-size: 18px;">'
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

# Generate HTML based on contour shapes
html_output = generate_html_page(contours)

# Save the HTML to a file
with open('handdrawn.html', 'w') as f:
    f.write(html_output)
