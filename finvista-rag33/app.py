# import os
# import streamlit as st
# from dotenv import load_dotenv
# from agent import process_documents, load_vectorstore, get_agent_response

# load_dotenv()

# # Page config
# st.set_page_config(
#     page_title="FinVista Financial Assistant",
#     page_icon="💹",
#     layout="wide"
# )

# st.title("💹 FinVista Financial Intelligence Assistant")
# st.markdown("Ask questions about your financial documents!")

# # Initialize session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None

# # Sidebar for document upload
# with st.sidebar:
#     st.header("📄 Upload Documents")
#     uploaded_files = st.file_uploader(
#         "Upload PDF files",
#         type=["pdf"],
#         accept_multiple_files=True
#     )
    
#     if uploaded_files:
#         if st.button("Process Documents"):
#             with st.spinner("Processing documents..."):
#                 # Save files temporarily
#                 pdf_paths = []
#                 os.makedirs("temp_docs", exist_ok=True)
#                 for file in uploaded_files:
#                     path = f"temp_docs/{file.name}"
#                     with open(path, "wb") as f:
#                         f.write(file.getbuffer())
#                     pdf_paths.append(path)
                
#                 # Process and store in ChromaDB
#                 st.session_state.vectorstore = process_documents(pdf_paths)
#                 st.success(f"✅ {len(uploaded_files)} document(s) processed!")

#     # Load existing vectorstore
#     if st.button("Load Existing Documents"):
#         with st.spinner("Loading..."):
#             st.session_state.vectorstore = load_vectorstore()
#             st.success("✅ Documents loaded!")

# # Chat interface
# st.header("💬 Chat")

# # Display chat history
# for human, ai in st.session_state.chat_history:
#     with st.chat_message("user"):
#         st.write(human)
#     with st.chat_message("assistant"):
#         st.write(ai)

# # User input
# question = st.chat_input("Ask a question about your documents...")

# if question:
#     if st.session_state.vectorstore is None:
#         st.error("Please upload and process documents first!")
#     else:
#         with st.chat_message("user"):
#             st.write(question)
        
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response, sources = get_agent_response(
#                     question,
#                     st.session_state.chat_history,
#                     st.session_state.vectorstore
#                 )
#                 st.write(response)
                
#                 # Show source citations
#                 if sources:
#                     with st.expander("📚 Sources"):
#                         for i, doc in enumerate(sources):
#                             st.write(f"**Source {i+1}:** {doc.metadata.get('source', 'Unknown')}")
#                             st.write(f"**Page:** {doc.metadata.get('page', 'Unknown')}")
#                             st.write("---")
        
#         # Update chat history
#         st.session_state.chat_history.append((question, response))

import os
import streamlit as st
from dotenv import load_dotenv
from agent import process_documents, load_vectorstore, get_agent_response

load_dotenv()

# Page config
st.set_page_config(
    page_title="FinVista Financial Assistant",
    page_icon="💹",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: #16213e;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0f3460;
        margin: 5px 0;
    }
    .success-box {
        background: #1a472a;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {}

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin:0;">💹 FinVista Financial Intelligence Assistant</h1>
    <p style="color: #a0aec0; margin:0;">Powered by RAG + Groq AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📄 Document Management")
    
    # Upload section
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("⚙️ Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                pdf_paths = []
                os.makedirs("temp_docs", exist_ok=True)
                for file in uploaded_files:
                    path = f"temp_docs/{file.name}"
                    with open(path, "wb") as f:
                        f.write(file.getbuffer())
                    pdf_paths.append(path)
                
                st.session_state.vectorstore = process_documents(pdf_paths)
                st.session_state.doc_stats = {
                    "files": len(uploaded_files),
                    "names": [f.name for f in uploaded_files]
                }
                st.success(f"✅ {len(uploaded_files)} document(s) processed!")

    if st.button("📂 Load Existing Documents"):
        with st.spinner("Loading..."):
            st.session_state.vectorstore = load_vectorstore()
            st.success("✅ Documents loaded!")

    st.divider()

    # Document Statistics
    if st.session_state.doc_stats:
        st.header("📊 Document Statistics")
        st.metric("Files Uploaded", st.session_state.doc_stats.get("files", 0))
        st.metric("Messages in Chat", len(st.session_state.chat_history))
        
        st.subheader("📁 Loaded Files:")
        for name in st.session_state.doc_stats.get("names", []):
            st.write(f"• {name}")

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat cleared!")
        st.rerun()

    st.divider()

    # About section
    st.header("ℹ️ About")
    st.markdown("""
    **FinVista Capital**  
    Enterprise Financial Intelligence Assistant
    
    **Tech Stack:**
    - 🤖 LLM: Groq (llama-3.3-70b)
    - 🔢 Embeddings: HuggingFace
    - 📦 Vector DB: ChromaDB
    - 🖥️ UI: Streamlit
    """)

# Main chat area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat")

    # Status indicator
    if st.session_state.vectorstore:
        st.success("✅ Documents loaded — Ready to answer questions!")
    else:
        st.warning("⚠️ Please upload and process documents first!")

    # Display chat history
    for human, ai in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(human)
        with st.chat_message("assistant"):
            st.write(ai)

    # User input
    question = st.chat_input("Ask a question about your documents...")

    if question:
        if st.session_state.vectorstore is None:
            st.error("Please upload and process documents first!")
        else:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response, sources = get_agent_response(
                        question,
                        st.session_state.chat_history,
                        st.session_state.vectorstore
                    )
                    st.write(response)

                    # Show source citations
                    if sources:
                        with st.expander("📚 View Sources"):
                            for i, doc in enumerate(sources):
                                st.markdown(f"**Source {i+1}:**")
                                st.write(f"📄 File: {doc.metadata.get('source', 'Unknown')}")
                                st.write(f"📃 Page: {doc.metadata.get('page', 'Unknown')}")
                                st.divider()

            st.session_state.chat_history.append((question, response))

with col2:
    st.header("📝 Conversation History")
    if st.session_state.chat_history:
        for i, (human, ai) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q{i+1}: {human[:40]}..."):
                st.write(f"**You:** {human}")
                st.write(f"**AI:** {ai}")
    else:
        st.info("No conversation history yet!")