from langchain_text_splitters import RecursiveCharacterTextSplitter
import nltk
from nltk.tokenize import word_tokenize

#nltk.download('punkt')
#nltk.download('punkt_tab')

# This is a long document we can split up.
with open("D:\\Me-hi\\20241\\CHATBOT\\Document\\Document.txt", encoding="utf-8") as f:
    state_of_the_union = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([state_of_the_union])
#print(texts[0])
#print(texts[1])
#print(texts[14])
#print(texts[40])


def search_keywords_in_texts(texts):
    found_keywords = []

    for i, text in enumerate(texts):
        text_content = text.page_content
        if len(word_tokenize(text_content)) < 10: 
            found_keywords.append(i)

    return found_keywords

result = search_keywords_in_texts(texts)
#print(result)

def group_texts_by_index(texts, found_keywords):
    grouped_texts = []
    found_keywords = sorted(found_keywords)  # Sắp xếp các chỉ số trong found_keywords

    # Nhóm các phần tử liên tiếp, bao gồm cả các phần tử từ found_keywords
    current_group = [found_keywords[0]]  # Bắt đầu nhóm với phần tử đầu tiên trong found_keywords

    for i in range(1, len(found_keywords)):
        if found_keywords[i] == found_keywords[i-1] + 1:  # Nếu có khoảng cách 1
            current_group.append(found_keywords[i])  # Thêm vào nhóm hiện tại
        else:
            grouped_texts.append(list(range(current_group[0], found_keywords[i])))  # Nhóm các phần tử từ current_group[0] đến found_keywords[i]-1
            current_group = [found_keywords[i]]  # Bắt đầu nhóm mới với phần tử hiện tại

    # Thêm nhóm cuối cùng vào nếu có
    if current_group:
        grouped_texts.append(list(range(found_keywords[-1], len(texts))))   # Nhóm phần tử cuối cùng

    return grouped_texts


grouped_texts = group_texts_by_index(texts, result)
#print(grouped_texts)

for group in grouped_texts:
    # Lấy thông tin sản phẩm từ text[group[0]]
    product_info = texts[group[0]]
    # Gắn nhãn cho tất cả các text trong nhóm, bỏ qua text[group[0]]
    for idx in group[1:]:
        texts[idx].page_content = f"[Product code: {product_info.page_content}] {texts[idx].page_content}"
    texts[group[0]] = None  # Đánh dấu là None để xóa sau

# Loại bỏ tất cả các phần tử None trong text
texts = [t for t in texts if t is not None]

#print(texts)

#for group in grouped_texts:
    #print([texts[i].page_content for i in group])