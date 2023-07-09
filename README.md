# License Plate Detection and OCR

This script performs license plate detection and optical character recognition (OCR) on images using OpenCV and pytesseract.

## Dependencies

- OpenCV
- imutils
- pytesseract

## Setup

1. Install the required dependencies by running the following command:
   ```
   pip install opencv-python imutils pytesseract
   ```

2. Download and install Tesseract OCR from the [official website](https://github.com/tesseract-ocr/tesseract).

3. Update the `path` variable in the script with the paths of the images you want to process.

4. Run the script using Python:
   ```
   python license_plate_detection.py
   ```

## Output

The script performs the following steps:
1. Reads an image and preprocesses it by resizing, converting to grayscale, and applying filters.
2. Detects the license plate contours and filters out the possible license plate shape.
3. Masks out the license plate and crops the image.
4. Performs OCR on the license plate using pytesseract.
5. Draws the bounding box and displays the license plate number on the original image.
6. Saves the license plate number in a text file.

The detected license plate number is displayed, and the image with the license plate and number is shown.

Please note that the accuracy of OCR may vary depending on the image quality and license plate characteristics.

## License

This project is licensed under the [MIT License](LICENSE).
