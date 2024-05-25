import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('C:\\Users\\HP\\Desktop\\probni_set\\hand6.jpg')

# Resize the image
desired_width = 1000
desired_height = 700
scaled_image = cv2.resize(image, (desired_width, desired_height))

# Convert the image to grayscale
gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Find edges using Canny edge detection
edged = cv2.Canny(blurred_image, 30, 200)

# Find contours and hierarchy
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours (noise)
min_contour_area = 50  # Adjust this threshold as needed
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Draw contours on the original image
contour_image = scaled_image.copy()
cv2.drawContours(contour_image, filtered_contours, -1, (0, 255, 0), 3)

# Display the results
plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
plt.title('Contours')
plt.show()

print("Number of Contours found = " + str(len(filtered_contours)))

# Iterate through contours and hierarchy
for idx, (contour, hier) in enumerate(zip(filtered_contours, hierarchy[0])):
    # Check if contour has child
    if hier[2] != -1:
        print(f"Contour {idx + 1} has child")
    else:
        print(f"Contour {idx + 1} has no child")

def analyze_contours_and_generate_html(contours):
    html = ""
    for idx, contour in enumerate(contours):
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)

        # Generate HTML based on contour properties
        html += f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; border: 2px solid red;">'
        html += f'Area: {area}<br>'
        html += f'Number of Vertices: {num_vertices}<br>'
        html += '</div><br>'

    return html

# Generate HTML based on contour shapes
html_output = analyze_contours_and_generate_html(contours)

# Save the HTML to a file or display it
with open('output5.html', 'w') as f:
    f.write(html_output)

def generate_html_page(contours):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Contour Analysis</title>
    </head>
    <body>
    """

    for idx, contour in enumerate(contours):
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)

        if num_vertices == 4 and area > 100:  # Check if contour is a quadrilateral
            if area < 10000:  # Check if area is less than 10000
                # Generate button HTML at the location of the contour
                html += f'<button style="position: absolute; left: {x}px; top: {y}px;">Click Me</button>'
            elif area > 10000 and h / w < 0.5:
                html += f'<input id="input{idx}" class="draggable" type="text" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px;">'
            else:
                # Check for child contours with 3 or more vertices
                for child_contour in contours:
                    if len(cv2.approxPolyDP(child_contour, 0.04 * cv2.arcLength(child_contour, True), True)) >= 3:
                        # Draw an image at the location of the parent contour
                        html += f'<img src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="Custom Shape" style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px;">'
                        break  # Break the loop after drawing one image
        elif num_vertices == 2 and area > 100:
            html += f'<p style="position: absolute; left: {x}px; top: {y}px; font-size: 18px;">Some Text</p>'

    html += """
    </body>
    </html>
    """
    return html

# Generate HTML based on contour shapes
html_output = generate_html_page(contours)

# Save the HTML to a file
with open('handdrawn.html', 'w') as f:
    f.write(html_output)
