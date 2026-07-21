import uvicorn
from fastapi import FastAPI, File, UploadFile
from paddleocr import PaddleOCR
import cv2
import numpy as np

app = FastAPI()

# 使用 PP-OCRv6 模型和 ONNX Runtime 引擎[reference:9]
ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv6_tiny_det",   # 可选: tiny_det, small_det, medium_det
    text_recognition_model_name="PP-OCRv6_tiny_rec", # 可选: tiny_rec, small_rec, medium_rec
    engine="onnxruntime",
    use_textline_orientation=True,
    lang='ch'  # 'ch' 表示中英文模型
)

@app.post('/ocr')
async def ocr_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {'error': 'Invalid image'}
    result = ocr.predict(img)
    text_lines = []
    if result and result[0]:
        for line in result[0]:
            text_lines.append(line[1][0])
    text = '\n'.join(text_lines)
    return {'text': text}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)