#!/bin/bash

RUN_PORT=${PORT:-8000}

uvicorn app.main:app --bind "0.0.0.0:${RUN_PORT}"