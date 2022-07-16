import pathlib
import io
import uuid
import pytesseract

from fastapi import FastAPI, HTTPException, Request, Depends, File, UploadFile, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from functools import lru_cache

from .fastapi_settings import Settings
from .ocr import apply_ocr, read_img


# Define the base directory
BASE_DIR = pathlib.Path(__file__).parent.parent

# Define directory for uploads
UPLOAD_DIR = BASE_DIR / "uploads"

# Instantiate the FastAPI object
app = FastAPI()

# Set up and point to the templates directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Return the Settings instance and store it in cache for efficient retrieval
@lru_cache
def get_settings():
    return Settings()


# Home view -> http GET
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Image-to-text endpoint -> http POST
@app.post("/convert")
async def post_image_to_text(file: UploadFile = File(...)):
    img = await read_img(file, HTTPException(status_code=422, detail="Invalid image"))

    ocr_predictions: str = pytesseract.image_to_string(img)

    return {
        "results": {
            "raw": ocr_predictions,
            "cleaned": ocr_predictions.replace("\n", " ").strip(),
            "lines": ocr_predictions.split("\n"),
        }
    }


# Image upload test endpoint -> http POST
@app.post("/img-echo", response_class=FileResponse)
async def image_echo_view(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    if not settings.echo_active:
        raise HTTPException(
            detail="Invalid endpoint!", status_code=status.HTTP_400_BAD_REQUEST
        )

    # Make the uploads dir if doesn't exist
    UPLOAD_DIR.mkdir(exist_ok=True)

    # Read the bytes of the file
    byte_str = io.BytesIO(await file.read())

    # Extract metadata
    fname = pathlib.Path(file.filename)  # name of uploaded file
    fext = fname.suffix  # extension of uploaded file
    abs_fname = str(fname).split(fext)[0]  # name of file without the ext

    # Generate a unique destination for uploaded file
    destination = UPLOAD_DIR / f"{abs_fname}-{uuid.uuid1()}{fext}"

    # Save uploaded file at the generated destination
    with open(str(destination), "wb") as out:
        out.write(byte_str.read())

    # Return file
    return destination
