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

    # --- 修改开始 ---
    # 使用更通用的方式提取所有识别出的文本
    text_lines = []
    if result:
        # result 是一个列表，包含每张图片的识别结果（这里只有一张图）
        for res in result:
            # 从每个结果中提取 'rec_texts' 字段，它包含了所有识别出的文本行
            if 'rec_texts' in res:
                text_lines.extend(res['rec_texts'])
            # 如果字段名不同，也可以尝试用 'rec_text' 或其他可能的键
            # elif 'rec_text' in res:
            #     text_lines.append(res['rec_text'])

    text = '\n'.join(text_lines)
    # --- 修改结束 ---

    return {'text': text}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)