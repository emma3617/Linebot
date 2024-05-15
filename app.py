import os
from flask import Flask, request, jsonify, abort, render_template, redirect, url_for
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackEvent
from pymongo import MongoClient
import logging
from openai import OpenAI
import httpx

# 設置 Flask 應用
app = Flask(__name__)

# 設置 LINE Bot
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 設置 MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.book_bot_db
##在DB建立的兩個資料庫儲存用戶資料以及書本資訊
books_collection = db.books
users_collection = db.users

# 設置日誌
logging.basicConfig(level=logging.INFO)

# 設置自定義 OpenAI 客戶端
http_client = httpx.Client(base_url="Your_OpenAI_URL",follow_redirects=False)
client2 = OpenAI(
    base_url="Your_API_KEY", 
    api_key="Your_API_KEY",
    http_client=http_client,
)

# 插入書籍資料的端點
@app.route('/books', methods=['POST'])
def add_book():
    data = request.form
    if not data or 'title' not in data or 'author' not in data:
        abort(400, 'Invalid data')
    
    book = {
        'title': data['title'],
        'author': data['author'],
        'genre': data.get('genre'),
        'description': data.get('description')
    }
    
    ##把上面定義的資料欄位灌進DB
    books_collection.insert_one(book)
    
    # 查找偏好該類型書籍的所有用戶
    genre = book['genre']
    users = users_collection.find({'preferences': genre})
    user_ids = [user['user_id'] for user in users]
    
    # 推送消息給所有這些用戶
    if user_ids:
        reply_text = f"新增了一本屬於 {genre} 類型的書籍：{book['title']}"
        
        for user_id in user_ids:
            line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))
    
    return redirect(url_for('index'))

# 查詢書籍資料的端點
@app.route('/books', methods=['GET'])
def get_books():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400, 'User ID is required')
    
    user = users_collection.find_one({'user_id': user_id})
    if not user or 'preferences' not in user:
        abort(404, 'User not found or preferences not set')

    preferences = user['preferences']
    recommended_books = books_collection.find({'genre': {'$in': preferences}})
    
    books = []
    for book in recommended_books:
        books.append({
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'description': book.get('description')
        })
    
    return jsonify({'recommended_books': books}), 200

# 查詢相同類型書籍的端點
@app.route('/books/<genre>', methods=['GET'])
def get_books_by_genre(genre):
    books = books_collection.find({'genre': genre})
    book_titles = [book['title'] for book in books]
    
    return jsonify({'books': book_titles}), 200

# 查詢所有書籍類型的端點
@app.route('/genres', methods=['GET'])
def get_genres():
    genres = books_collection.distinct('genre')
    return jsonify({'genres': genres}), 200

# 前端界面
@app.route('/')
def index():
    return render_template('index.html')

# LINE Bot 回調處理
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Check your channel secret/access token.")
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text
    
    if user_message.startswith("偏好"):
        user_message = user_message.split(" ")[-1]
        # 假設處理用戶的偏好更新：
        users_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'preferences': user_message}},
            upsert=True
        )

        # 查找相同類型的書籍
        books = books_collection.find({'genre': user_message})
        book_titles = [book['title'] for book in books]
        
        if book_titles:
            reply_text = f"以下是一些屬於 {user_message} 類型的書籍：\n" + "\n".join(book_titles)
        else:
            reply_text = f"目前沒有屬於 {user_message} 類型的書籍。"
    
    elif user_message == "查看偏好":
        user = users_collection.find_one({'user_id': user_id})
        if user and 'preferences' in user:
            preferences = user['preferences']
            reply_text = "你目前的偏好類型有：" + ", ".join(preferences)
        else:
            reply_text = "你還沒有設置任何偏好。"
    
    elif user_message.startswith("刪除偏好"):
        preference_to_delete = user_message.split(" ")[-1]
        users_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'preferences': preference_to_delete}}
        )
        reply_text = f"已刪除偏好：{preference_to_delete}"

    elif user_message == "查詢書籍類型":
        genres = books_collection.distinct('genre')
        reply_text = "目前書籍類型有：" + ", ".join(genres)

    elif user_message.startswith("找書"):
        genre = user_message.split(" ")[-1]
        books = books_collection.find({'genre': genre})
        book_titles = [book['title'] for book in books]
        
        if book_titles:
            reply_text = f"目前 {genre} 類型的書籍有：\n" + "\n".join(book_titles)
        else:
            reply_text = f"目前沒有屬於 {genre} 類型的書籍。"

    elif user_message.startswith("介紹"):
        try:
            response = client2.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "詳細介紹" +user_message + "請用繁體中文回應"}
                ]
            )
            if response:
                reply_text = response.choices[0].message.content.strip()
            else:
                reply_text = f"{response}{type(response)}"
        except Exception as e:
            app.logger.error(f"OpenAI API error: {e}")
            reply_text = "抱歉，我無法處理您的請求。請稍後再試。"

    else:
        # 使用 GPT 處理非關鍵詞問題
        try:
            response = client2.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message + "請用繁體中文回應"}
                ]
            )
            if response:
                reply_text = response.choices[0].message.content.strip()
            else:
                reply_text = f"{response}{type(response)}"
        except Exception as e:
            app.logger.error(f"OpenAI API error: {e}")
            reply_text = "抱歉，我無法處理您的請求。請稍後再試。"

    reply = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, reply)
    return 'OK', 200  # 確保回傳 HTTP 200 狀態

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    
    if data == "查看偏好":
        user = users_collection.find_one({'user_id': user_id})
        if user and 'preferences' in user:
            preferences = user['preferences']
            reply_text = "你目前的偏好類型有：" + ", ".join(preferences)
        else:
            reply_text = "你還沒有設置任何偏好。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    elif data.startswith("刪除偏好"):
        preference_to_delete = data.split("=")[-1]
        users_collection.update_one(
            {'user_id': user_id},
            {'$pull': {'preferences': preference_to_delete}}
        )
        reply_text = f"已刪除偏好：{preference_to_delete}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    return 'OK', 200  # 確保回傳 HTTP 200 狀態

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
