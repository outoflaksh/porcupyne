#!/bin/bash

RUN_PORT=${PORT:-8000}

uvicorn src.app.main:app --host '0.0.0.0' --port ${RUN_PORT}