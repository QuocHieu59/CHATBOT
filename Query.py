from pymongo import MongoClient
import re
import spacy

# try:
#     # Tạo kết nối đến MongoDB
#     client = MongoClient('mongodb://localhost:27017/')
#     print("Successful connection to MongoDB!")
# except Exception as e:
#     # Xử lý ngoại lệ nếu có lỗi xảy ra
#     print("MongoDB connection failed")
#     print("Lỗi:", e)
# db = client['GoMyNghe']
# collection = db['tuonggo360']

# Load mô hình NLP (sử dụng spaCy)
nlp = spacy.load('en_core_web_md')  

# Danh sách các thuộc tính có thể
ATTRIBUTES = {
    "price": "price",
    "cost": "price",
    "name": "name",
    "color": "color",
    "weight": "mass",
    "mass": "mass",
    "call": "hotline",
    "hotline": "hotline",
}

def extract_query(question):
     # Tìm mã sản phẩm bằng regex
    product_id_match = re.search(r'#([A-Za-z0-9\-]+)', question)
    product_id = product_id_match.group(1) if product_id_match else None

    # Phân tích câu hỏi bằng NLP
    doc = nlp(question.lower())
    
    # Tìm thuộc tính trong câu hỏi
    attribute = None
    for token in doc:
        if token.text in ATTRIBUTES.keys():
            attribute = ATTRIBUTES[token.text]
            break

    # Nếu không tìm thấy thuộc tính
    if not attribute:
        attribute = False  

    return product_id, attribute

# def query_database(product_id, attribute):
#     """
#     Truy vấn MongoDB dựa trên mã sản phẩm và thuộc tính.
#     """
#     global Prompt  # Sử dụng biến toàn cục
#     if not product_id or not attribute:
#         return "Không thể xác định thông tin từ câu hỏi."

#     # Tìm sản phẩm trong cơ sở dữ liệu
#     product = collection.find_one({"code": product_id})
    
#     if not product:
#         return f"Shop currently has no products with the code #{product_id}."

#     # Trả về thuộc tính được yêu cầu
#     if attribute in product:
#         Prompt = Prompt + " " + f"Sản phẩm #{product_id} có {attribute} là {product[attribute]}."
#         return f"Sản phẩm #{product_id} có {attribute} là {product[attribute]}."

# def handle_question(question):
#     """
#     Hàm chính để xử lý câu hỏi người dùng.
#     """
#     product_id, attribute = extract_query(question)
#     #print(product_id, attribute)
#     response = query_database(product_id, attribute)
#     return response

# # Ví dụ câu hỏi người dùng
# questions = [
#    "How much does product #OA-66 cost?",
#     "What is the color of product #OA-66?",
#     "If I want to request a special product #OA-66, what is the manufacturer's hotline number?",
#     "Where is product #OA-20 produced?",
# ]

# for question in questions:
#     print(handle_question(question))
#     print(Prompt)
