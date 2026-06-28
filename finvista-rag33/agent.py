import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# LLM
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=os.getenv("GROQ_MODEL", "llama3-8b-8192")
    )

# Embeddings
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

# Process PDF and store in ChromaDB
def process_documents(pdf_files):
    documents = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    
    # Chunk documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    
    # Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory="./chroma_db"
    )
    vectorstore.persist()
    return vectorstore

# Load existing vectorstore
def load_vectorstore():
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=get_embeddings()
    )

# Get agent response
# def get_agent_response(question, chat_history, vectorstore):
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=True,
#         output_key="answer"
#     )
    
#     # Add existing history to memory
#     for human, ai in chat_history:
#         memory.chat_memory.add_user_message(human)
#         memory.chat_memory.add_ai_message(ai)
    
#     chain = ConversationalRetrievalChain.from_llm(
#         llm=get_llm(),
#         retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
#         memory=memory,
#         return_source_documents=True
#     )
    
#     result = chain({"question": question})
#     return result["answer"], result["source_documents"]

def get_agent_response(question, chat_history, vectorstore):
    llm = get_llm()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful financial assistant for FinVista Capital.
    Use the following context to answer the question.
    Always provide clear and concise answers with source citations.
    
    Context: {context}
    
    Question: {question}
    """)
    
    # Get relevant documents
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Generate response
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    return response, docs




# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_community.document_loaders import PyPDFLoader

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory

# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import HumanMessage, AIMessage

# load_dotenv()

# # LLM
# def get_llm():
#     return ChatGroq(
#         api_key=os.getenv("GROQ_API_KEY"),
#         model=os.getenv("GROQ_MODEL", "llama3-8b-8192")
#     )

# # Embeddings
# def get_embeddings():
#     return HuggingFaceEmbeddings(
#         model_name="all-MiniLM-L6-v2"
#     )

# # Process PDF and store in ChromaDB
# def process_documents(pdf_files):
#     documents = []
#     for pdf_path in pdf_files:
#         loader = PyPDFLoader(pdf_path)
#         documents.extend(loader.load())
    
#     # Chunk documents
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_documents(documents)
    
#     # Store in ChromaDB
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=get_embeddings(),
#         persist_directory="./chroma_db"
#     )
#     vectorstore.persist()
#     return vectorstore

# # Load existing vectorstore
# def load_vectorstore():
#     return Chroma(
#         persist_directory="./chroma_db",
#         embedding_function=get_embeddings()
#     )

# # Get agent response
# # def get_agent_response(question, chat_history, vectorstore):
# #     memory = ConversationBufferMemory(
# #         memory_key="chat_history",
# #         return_messages=True,
# #         output_key="answer"
# #     )
    
# #     # Add existing history to memory
# #     for human, ai in chat_history:
# #         memory.chat_memory.add_user_message(human)
# #         memory.chat_memory.add_ai_message(ai)
    
# #     chain = ConversationalRetrievalChain.from_llm(
# #         llm=get_llm(),
# #         retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
# #         memory=memory,
# #         return_source_documents=True
# #     )
    
# #     result = chain({"question": question})
# #     return result["answer"], result["source_documents"]

# def get_agent_response(question, chat_history, vectorstore):
#     llm = get_llm()
#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
#     prompt = ChatPromptTemplate.from_template("""
#     You are a helpful financial assistant for FinVista Capital.
#     Use the following context to answer the question.
#     Always provide clear and concise answers with source citations.
    
#     Context: {context}
    
#     Question: {question}
#     """)
    
#     # Get relevant documents
#     docs = retriever.invoke(question)
#     context = "\n\n".join([doc.page_content for doc in docs])
    
#     # Generate response
#     chain = prompt | llm | StrOutputParser()
#     response = chain.invoke({
#         "context": context,
#         "question": question
#     })
    
#     return response, docs
