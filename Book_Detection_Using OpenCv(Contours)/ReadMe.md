## Book Detection from Webcam Feed

This project aims to detect books in images captured from a webcam feed using OpenCV (cv2). The image processing pipeline involves converting the image to grayscale, applying adaptive thresholding, and performing edge detection. Contours are then identified in the processed image. If a contour is detected with four sides, it is classified as a book and highlighted with a green rectangle.

**Note**: The current implementation achieves book detection based on contour analysis, but the accuracy is low as it may detect any rectangle object as a book. Further refinement and model development are necessary to improve accuracy and specificity.
