# 🌸 Linebot 🌸

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/emma3617/Linebot/blob/master/README.md)
[![zh-tw](https://img.shields.io/badge/lang-zh--tw-green.svg)](https://github.com/emma3617/Linebot/blob/master/README.zh-tw.md)

A Python-based Line bot application designed to provide automated responses and interactions via the Line messaging platform.

## ✨ Features ✨

- **Automated Replies:** Configurable responses to user messages.
- **Web Integration:** Utilizes Flask to handle webhook events from Line.
- **OpenAI API Integration:** Utilizes OpenAI's API to generate responses and handle user queries.
- **MongoDB Support:** Stores user and book information.
- **Docker Support:** Easily deployable using Docker.

## 🚀 Installation 🚀

1. **Clone the repository:**
    ```bash
    git clone https://github.com/emma3617/Linebot.git
    cd Linebot
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```bash
    python app.py
    ```

## 📚 Usage 📚

1. **Setup Line Bot:** Register your bot on the [Line Developers](https://developers.line.biz/en/) platform and obtain the necessary credentials.
2. **Configure Environment Variables:** Set your Line bot credentials, MongoDB URI, and OpenAI API key in the environment.
3. **Deploy:** Use Docker for easy deployment:
    ```bash
    docker build -t linebot .
    docker run -p 5000:5000 linebot
    ```
4. **Run Docker Container:**
    ```bash
    docker run -d -p 5000:5000 --name linebot_container linebot
    ```

## 📁 Files 📁

- `app.py`: Main application code.
- `requirements.txt`: List of dependencies.
- `Dockerfile`: Configuration for Docker container.
- `templates/`: HTML templates.
- `static/`: Static files (CSS, JavaScript).

## 🤝 Contributing 🤝

Feel free to open issues or submit pull requests for improvements or bug fixes.

## 📄 License 📄

This project is licensed under the MIT License.
