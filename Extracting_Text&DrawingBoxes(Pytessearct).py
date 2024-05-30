import cv2
import pytesseract
import matplotlib.pyplot as plt

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to capture an image
def capture_image(event, x, y, flags, param):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        img = frame.copy()

# Create a window to display the webcam feed
cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", capture_image)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Calculate the dimensions for the 3:4 aspect ratio box
    aspect_ratio = 3 / 4
    frame_height, frame_width, _ = frame.shape
    box_width = min(frame_width, int(frame_height * aspect_ratio))
    box_height = min(frame_height, int(frame_width / aspect_ratio))

    # Calculate the top-left corner coordinates for the box to be at the center
    top_left_x = (frame_width - box_width) // 2
    top_left_y = (frame_height - box_height) // 2

    # Calculate the bottom-right corner coordinates for the box
    bottom_right_x = top_left_x + box_width
    bottom_right_y = top_left_y + box_height

    # Draw a green box in the calculated coordinates
    cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

    # Display the frame in the window
    cv2.imshow("Webcam", frame)

    # Check for the 'q' key to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

# Save the captured image
if 'img' in globals():
    cv2.imwrite("captured_image.png", img)
    print("Image captured and saved as captured_image.png.")
else:
    print("No image captured.")

# Load the image
image = cv2.imread("captured_image.png")

# Crop the image to the green box region
cropped_image = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

# Convert to grayscale
gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# Perform edge detection
edged = cv2.Canny(gray, 10, 250)

# Perform morphological operations to close gaps in between object edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

# Use Tesseract to extract text and bounding boxes
h, w, c = cropped_image.shape
boxes = pytesseract.image_to_boxes(cropped_image)
for b in boxes.splitlines():
    b = b.split(' ')
    cropped_image = cv2.rectangle(cropped_image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# Display the image with bounding boxes
plt.figure(figsize=(15, 20))
plt.imshow(cropped_image)
plt.show()

# Extract text with custom configuration
custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
text = pytesseract.image_to_string(cropped_image, config=custom_config)
print(text)
