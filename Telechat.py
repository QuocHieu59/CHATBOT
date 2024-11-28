from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import nest_asyncio
import re
import spacy
from pymongo import MongoClient
from openai import OpenAI
from Query import extract_query

# Định nghĩa Prompt
Prompt = "You are a fine art wood sales consultant. Please answer user questions"

# Tạo kết nối đến MongoDB

try:
    client = MongoClient('mongodb://localhost:27017/')
    print("Successful connection to MongoDB!")
except Exception as e:
    # Xử lý ngoại lệ nếu có lỗi xảy ra
    print("MongoDB connection failed")
    print("Lỗi:", e)
db = client['GoMyNghe']
collection = db['tuonggo360']

# Kết nối tới máy chủ mô hình AI cục bộ
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Khắc phục lỗi vòng lặp sự kiện
nest_asyncio.apply()

# Load mô hình NLP (sử dụng spaCy)
nlp = spacy.load('en_core_web_md')  

#query with code
def query_database(product_id, attribute):
    global Prompt
    if not product_id or not attribute:
        return
    # Tìm sản phẩm trong cơ sở dữ liệu
    product = collection.find_one({"code": product_id})
    
    if not product:
        Prompt = Prompt + ". " +  f"NotShop currently has no products with the code #{product_id}."
        return
    
    # Trả về thuộc tính được yêu cầu
    if attribute in product:
        Prompt = Prompt + ". " + f"Note Product #{product_id} {attribute} là {product[attribute]}."
        return 
    
# Hàm generate_response để xử lý yêu cầu và trả về phản hồi
async def generate_response(product_id, attribute, user_input: str) -> str:
    global Prompt
    query_database(product_id, attribute)
    # Gửi yêu cầu tới mô hình AI
    completion = client.chat.completions.create(
        model="local-model",  # Tên mô hình (hiện không cần thiết)
        messages=[
            {"role": "system", "content": Prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        stream=True,
    )

    Prompt = "You are a fine art wood sales consultant. Please answer user questions"

    # Kết hợp phản hồi từ các đoạn stream
    response_content = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response_content += chunk.choices[0].delta.content

    return response_content


# Hàm xử lý khi người dùng gửi lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am a chatbot that supports consulting on wood handicraft sales. Please submit your question.")

# Hàm xử lý tin nhắn từ người dùng
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    product_id, attribute = extract_query(user_input)
    response = await generate_response(product_id, attribute, user_input)
    await update.message.reply_text(response)

# Hàm chính để khởi động bot
def main():
    TOKEN = '7998426748:AAFfSz6eJZGyM5-E_h42et21UMGOPiCgPcE'            # API lấy từ BotFather
    app = Application.builder().token(TOKEN).build()

    # Thêm handler cho lệnh /start
    app.add_handler(CommandHandler("start", start))

    # Thêm handler cho tin nhắn văn bản
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Khởi động bot
    # Chạy bot bằng vòng lặp sự kiện hiện có
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run_polling())

if __name__ == '__main__':
    main()