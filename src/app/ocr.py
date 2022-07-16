import cv2
import io
import pytesseract

from PIL import Image
from numpy import asarray, ndarray
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
    img = asarray(img)

    return img


def resize_img(img: ndarray):
    # Resize image
    return cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)


def apply_ocr(img: ndarray):
    # Resize image to 300 dpi
    img = resize_img(img)

    preds: str = pytesseract.image_to_string(img)

    return preds
