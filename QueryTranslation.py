import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import os
import getpass
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.load import dumps, loads

# Multi Query: Different Perspectives
template = """You are an AI language model assistant. Your task is to generate three 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""

prompt_perspectives = ChatPromptTemplate.from_template(template)

generate_queries = (
    prompt_perspectives 
    | ChatOpenAI(model="gpt-3.5-turbo", temperature=0) 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

question = 'Suggest me a product have price under $100 that is on sale?'
prompt_input = {"question": question}
alternative_queries = generate_queries.invoke({"question": question})

# Print the results
for i, query in enumerate(alternative_queries, 1):
     print(f"Alternative {i}: {query}")
     
def get_unique_union(documents: list[list]):
    """ Unique union of retrieved docs """
    # Flatten list of lists, and convert each Document to string
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    # Get unique documents
    unique_docs = list(set(flattened_docs))
    # Return
    return [loads(doc) for doc in unique_docs]

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

db = Chroma(persist_directory="D:\\Me-hi\\20241\\CHATBOT\\Document", embedding_function=embeddings)

retriever = db.as_retriever(search_kwargs={"k": 3})

retrieval_chain = generate_queries | retriever.map() | get_unique_union
docs = retrieval_chain.invoke({"question":question})
#print(docs)
page_contents = [doc.page_content for doc in docs]

# In ra danh sách mới chứa các nội dung page_content
print(page_contents)