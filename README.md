<div align="center">

  <h3 align="center">Porcupyne</h3>

  <p align="center">
    Image-to-text OCR microservice built with Python using FastAPI and Tesseract
    <br />
    <a href="https://porcupyne.herokuapp.com/">View Docs</a>
    ·
    <a href="https://github.com/outoflaksh/porcupyne/issues/">Report Bug</a>
    ·
    <a href="https://github.com/outoflaksh/porcupyne/issues/">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Porcupyne is an image-to-text microservice, powered by Google Tesseract OCR, that can be easily incorporated in any application via a simple-to-use API built with FastAPI. The whole microservice is containerized using Docker, making it easier for anyone to set up a local copy and bend it to their needs.

The microservice also cleans and processes the uploaded images with OpenCV; improving the OCR predictions of the Tesseract model.

### Built With

- [Python](https://python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://tesseract-ocr.github.io/)
- [Docker](https://www.docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Usage

It's extremely easy to use the Porcupyne OCR service. One simply needs to upload an image file they want converted via an HTTP POST request to `https://porcupyne.herokuapp.com/convert/` and a JSON response with the results obtained after applying OCR will be recieved back.

The request body will be of the form of a multipart form.

You can use your preffered API client to test it out. Example Python usage is also provided below:

```sh
  python3 -m pip install requests
```

```py
  import requests

  url = "https://porcupyne.herokuapp.com/convert"
  img_path = "/downloads/img.png"
  files = {"file": open(img_path, "rb")}

  response = requests.post(url, files=files)

  if response.status_code == 200:
    print(response.json())
```

Output:

```sh
{
	"results": {
		"raw": "It was the best of\ntimes, it was the worst\nof times, it was the age\nof wisdom, it was the\nage of foolishness...\n\f",
		"cleaned": "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness...",
		"lines": [
			"It was the best of",
			"times, it was the worst",
			"of times, it was the age",
			"of wisdom, it was the",
			"age of foolishness...",
			"\f"
		]
	}
}
```

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install Docker. Instructions can be found [here in the official docs](https://docs.docker.com/engine/install/).

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/outoflaksh/porcupyne.git
   ```
2. Change into the base directory.
   ```sh
   cd porcupyne
   ```
3. Build the Docker image.
   ```sh
   docker build -t porcupyne .
   ```
4. Run the Docker container.
   ```sh
   docker run porcupyne
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>
