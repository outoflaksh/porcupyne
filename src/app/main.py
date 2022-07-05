import pathlib
import io
import uuid

from fastapi import FastAPI, HTTPException, Request, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from functools import lru_cache

from .fastapi_settings import Settings


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
def read_index(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("index.html", {"request": request})


# Image upload test endpoint -> http POST
@app.post("/img-echo", response_class=FileResponse)
async def image_echo_view(
    file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint!", status_code=400)

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
