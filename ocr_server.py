import uvicorn
from fastapi import FastAPI, File, UploadFile
from paddleocr import PaddleOCR
import cv2
import numpy as np

app = FastAPI()

# 只指定语言和引擎，让 PaddleOCR 自动选择合适的中文模型
ocr = PaddleOCR(
    engine='onnxruntime',            # 使用 ONNX Runtime 避免 Paddle 后端兼容问题
    use_textline_orientation=True,   # 替代 use_angle_cls
    lang='ch'                        # 指定中文，会自动使用 ch_PP-OCRv6 模型
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
            text_lines.append(line[1][0])   # line[1][0] 是识别的文本
    text = '\n'.join(text_lines)
    return {'text': text}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)