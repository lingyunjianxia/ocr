#!/bin/bash
pip install paddleocr==3.7.0 fastapi uvicorn python-multipart -i https://pypi.org/simple
python /app/ocr_server.py