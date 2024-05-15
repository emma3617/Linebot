# 使用官方 Python 映像
FROM python:3.9

# 設置環境變數
ENV LINE_CHANNEL_SECRET=Your_API_KEY
ENV LINE_CHANNEL_ACCESS_TOKEN=Your_API_KEY
ENV MONGODB_URI=Your_API_KEY
ENV OPENAI_API_KEY=Your_API_KEY

# 設置工作目錄
WORKDIR /app

# 複製需求文件
COPY requirements.txt requirements.txt

# 安裝需求
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式文件
COPY . .

# 暴露端口
EXPOSE 5000

# 運行應用程式
CMD ["python", "app.py"]
