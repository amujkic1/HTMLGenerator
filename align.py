import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('C:\\Users\\HP\\Desktop\\probni_set\\hand15.jpg')

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
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    html = ""
    for idx, contour in enumerate(contours):
        # Calculate contour properties
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
        html += f'Area: {area} (Percentage: {area_percentage:.2f}% of total)<br>'
        html += f'Ratio: {h/w}<br>'
        #html += f'Number of Vertices: {num_vertices}<br>'
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contour Analysis</title>
        <style>
            .container {
                display: flex;
                flex-wrap: wrap;
            }
            .element {
                margin: 5px;
                border: 1px solid black;
                flex-grow: 1;
                flex-shrink: 1;
                flex-basis: calc(33.33% - 10px); /* ili drugi odgovarajući broj */
            }
        </style>
    </head>
    <body>
    <div class="container">
    """

    for idx, contour in enumerate(contours):
        # Calculate contour properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        num_vertices = len(approx)

        if num_vertices >= 3 and area > 100:  # Check if contour is a quadrilateral
            if area < 5000 and num_vertices < 7:  # Check if area is less than 10000
                html += f'<div class="element" style="left: {x}px; top: {y}px;">Click Me</div>'
            elif area < 5000 and num_vertices >= 7:
                html += f'<div class="element" style="left: {x}px; top: {y}px; font-size: 18px;">Some Text</div>'
            elif area > 5000 and h / w < 0.5:
                html += f'<input class="element" type="text" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px;">'
            else:
                for child_contour in contours:
                    if len(cv2.approxPolyDP(child_contour, 0.04 * cv2.arcLength(child_contour, True), True)) >= 3:
                        html += f'<img class="element" src="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png" alt="Custom Shape" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px;">'
                        break  # Break the loop after drawing one image
        elif num_vertices == 2 and area > 100:
            html += '<ul class="element" style="font-size: 18px;">'
            html += '<li>List item</li>'
            html += '</ul>'

    html += """
    </div>
    </body>
    </html>
    """
    return html


# Generate HTML based on contour shapes
html_output = generate_html_page(contours)

# Save the HTML to a file
with open('handdrawn.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

