# 🌸 Linebot 🌸

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/emma3617/Linebot/blob/master/README.md)
[![zh-tw](https://img.shields.io/badge/lang-zh--tw-green.svg)](https://github.com/emma3617/Linebot/blob/master/README.zh-tw.md)

一個基於 Python 的 Line bot 應用程式，透過 Line 訊息平台提供自動回覆和互動。

## ✨ 功能 ✨

- **自動回覆：** 可配置對用戶訊息的回應。
- **網絡集成：** 使用 Flask 處理來自 Line 的 Webhook 事件。
- **OpenAI API 集成：** 使用 OpenAI 的 API 生成回應並處理用戶查詢。
- **MongoDB：** 存儲用戶和書籍信息。
- **Docker：** 可通過 Docker 部署。

## 🚀 安裝 🚀

1. **Git Clone：**
    ```bash
    git clone https://github.com/emma3617/Linebot.git
    cd Linebot
    ```

2. **安裝requirements：**
    ```bash
    pip install -r requirements.txt
    ```

3. **運行應用程序：**
    ```bash
    python app.py
    ```

## 📚 使用 📚

1. **設置 Line 機器人：** 在 [Line Developers](https://developers.line.biz/en/) 平台註冊您的機器人並獲取必要的憑證。
2. **配置環境變量：** 設置您的 Line 機器人憑證、MongoDB URI 和 OpenAI API 密鑰。
3. **部署：** 使用 Docker 容易部署：
    ```bash
    docker build -t linebot .
    docker run -p 5000:5000 linebot
    ```
4. **運行 Docker 容器：**
    ```bash
    docker run -d -p 5000:5000 --name linebot_container linebot
    ```

## 📁 文件 📁

- `app.py`: 主應用程序代碼。
- `requirements.txt`: 依賴項列表。
- `Dockerfile`: Docker 容器配置。
- `templates/`: HTML 模板。
- `static/`: 靜態文件（CSS、JavaScript）。

## 🤝 貢獻 🤝

歡迎提出問題或提交拉取請求以改進或修復錯誤。

## 📄 許可 📄

此項目根據 MIT 許可證授權。
