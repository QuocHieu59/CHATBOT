import os
import getpass
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from Chunking import texts

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI_Key:')
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

db = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory="D:\\Me-hi\\20241\\CHATBOT\\Document")

#db = Chroma(persist_directory="D:\\Me-hi\\20241\\CHATBOT\\Document", embedding_function=embeddings)

#test
query = "color #0A-69"
docs = db.similarity_search(query, k = 3)
if docs:
    print(docs)
else:
    print("No similar documents found.")