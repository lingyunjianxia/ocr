# 使用 PaddlePaddle 基础
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.3.0

# 设置环境变量，禁用可能引发问题的功能
ENV FLAGS_use_mkldnn=0
ENV FLAGS_use_dnnl=0

# 设置工作目录
WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
COPY ocr_server.py /app/ocr_server.py

RUN chmod +x /app/entrypoint.sh
# 安装 PaddleOCR 3.7.0 及 ONNX Runtime[reference:7]
RUN pip install paddleocr==3.7.0 fastapi uvicorn python-multipart onnxruntime -i https://pypi.org/simple

# 预下载中文模型（与运行时参数一致）
RUN python -c "from paddleocr import PaddleOCR; PaddleOCR(engine='onnxruntime', use_textline_orientation=True, lang='ch')"

EXPOSE 8001

# 设置容器启动时执行的命令
CMD ["/bin/bash", "/app/entrypoint.sh"]