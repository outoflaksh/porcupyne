import cv2
import io
import pytesseract

from PIL import Image
from numpy import asarray, ndarray, ones, uint8
from fastapi import UploadFile

# Utility code to handle image processing and OCR


async def read_img(img: UploadFile, read_exception):
    # Convert file into a byte stream
    byte_string = io.BytesIO(await img.read())

    # Validate image by attempting to open it with PIL
    try:
        img = Image.open(byte_string)
    except:
        raise read_exception

    # Convert to numpy array for opencv
    img_array = asarray(img)

    return img_array


def resize_img(img_array: ndarray):
    # Resize image
    return cv2.resize(img_array, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)


def convert_to_grayscale(img_array):
    img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    return img


def denoise_img(img_array):
    kernel = ones((1, 1), uint8)
    img = cv2.dilate(img_array, kernel, iterations=1)
    img = cv2.erode(img_array, kernel, iterations=1)

    return img


def blur_img(img_array):
    # Extract & blur the bg so that the text is highlighted
    bg = cv2.threshold(
        cv2.medianBlur(img_array, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    img = 255 - cv2.absdiff(img_array, bg)

    return img


def apply_ocr(img_array: ndarray):
    # Image processing for better predictions

    # 1. Resize image to 300 dpi
    img = resize_img(img_array)

    # 2. Convert image to grayscale
    img = convert_to_grayscale(img)

    # 3. Remove noise
    img = denoise_img(img)

    # 4. Blur & segment image
    img = blur_img(img)

    preds: str = pytesseract.image_to_string(img)

    return preds
