import uvicorn
from fastapi import FastAPI, File, UploadFile
from paddleocr import PaddleOCR
import cv2
import numpy as np

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

@app.post('/ocr')
async def ocr_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {'error': 'Invalid image'}
    # 使用 predict 替代弃用的 ocr，去掉 cls 参数
    result = ocr.predict(img)
    text_lines = []
    if result and result[0]:
        for line in result[0]:
            text_lines.append(line[1][0])
    text = '\n'.join(text_lines)
    return {'text': text}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)