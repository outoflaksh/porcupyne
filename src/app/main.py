import pathlib

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from functools import lru_cache

from .fastapi_settings import Settings


# Define the base directory
BASE_DIR = pathlib.Path(__file__).parent.parent

# Instantiate the FastAPI object
app = FastAPI()

# Set up and point to the templates directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Return the Settings instance and store it in cache for efficient retrieval
@lru_cache
def get_settings():
    return Settings()


# Home view -> HTTP GET
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("index.html", {"request": request})
