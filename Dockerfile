# 使用 PaddlePaddle 基础
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.3.1

# 设置工作目录
WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
COPY ocr_server.py /app/ocr_server.py

RUN chmod +x /app/entrypoint.sh && \
    pip install paddleocr==3.7.0 fastapi uvicorn python-multipart -i https://pypi.org/simple

EXPOSE 8001

# 设置容器启动时执行的命令
CMD ["/bin/bash", "/app/entrypoint.sh"]