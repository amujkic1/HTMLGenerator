import cv2

def process_image_and_generate_html(image):

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

    return filtered_contours
