# 使用 PaddlePaddle 基础
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.0.0

# --- 环境变量（用于解决兼容性问题 + 指定模型源） ---
# 禁用 OneDNN（避免 NotImplementedError）
ENV FLAGS_use_dnnl=0
# 指定从国内 aistudio 源下载模型（更稳定，避免 modelscope 的 404 错误）
ENV PADDLE_PDX_MODEL_SOURCE=aistudio
# 跳过启动时的网络连通性检查（但仍会下载，只是不阻塞）
ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

# 设置工作目录
WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
COPY ocr_server.py /app/ocr_server.py

RUN chmod +x /app/entrypoint.sh && \
    pip install paddleocr==3.7.0 fastapi uvicorn python-multipart -i https://pypi.org/simple

# ★★★ 关键步骤：预下载所有模型文件 ★★★
# 调用 PaddleOCR 初始化，触发下载检测、识别、方向分类等模型
# 模型将自动保存到 /root/.paddlex/official_models/ 中
RUN python -c "from paddleocr import PaddleOCR; PaddleOCR(use_textline_orientation=True, lang='ch')"

EXPOSE 8001

# 设置容器启动时执行的命令
CMD ["/bin/bash", "/app/entrypoint.sh"]