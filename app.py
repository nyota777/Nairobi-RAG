import os
import streamlit as st
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Gemini integration
from PIL import Image

# ---------------------------
# 🔑 Load environment variables
# ---------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is missing. Please set it in your `.env` file.")
    st.stop()

# ---------------------------
# 🎨 Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="Nairobi RAG Chatbot", page_icon="🌍", layout="wide")

# Sidebar info
st.sidebar.title("ℹ️ About this App")
st.sidebar.write("""
This is a **Retrieval-Augmented Generation (RAG) Chatbot** about  
**Nairobi City, its History, National Park, and Museums**.  

- 🔎 Retrieves information from custom documents (PDFs, blogs, YouTube transcripts).  
- 🤖 Uses **Gemini (Google AI)** to answer your questions.  
- 📚 Built with **LangChain, FAISS, HuggingFace embeddings, and Streamlit**.  
""")

# ---------------------------
# 🏞️ Header + Images
# ---------------------------
st.title("🌍 Nairobi Tourist Attractions Chatbot")
st.write("Ask me anything about **Nairobi City, National Park, Museums, or History**!")

st.markdown("### 🏞️ Explore Nairobi visually")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images = {
    "Nairobi Skyline": "nairobi_skyline.jpg",
    "Nairobi National Park": "national_park.jpg",
    "National Museum of Kenya": "museum.jpg"
}

cols = st.columns(3)
for (caption, filename), col in zip(images.items(), cols):
    path = os.path.join(BASE_DIR, "images", filename)
    if os.path.exists(path):
        col.image(path, caption=caption, use_column_width=True)
    else:
        col.warning(f"⚠️ Image missing: {filename}")

st.markdown("---")

# ---------------------------
# 📂 Load FAISS Index
# ---------------------------
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    try:
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"❌ Could not load FAISS index. Did you run the indexing script?\n\nError: {e}")
        st.stop()

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ---------------------------
# 🤖 Build RAG Chain with Gemini
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # ✅ Use a valid Gemini model (fast + cost-effective)
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# ---------------------------
# 💬 User Input + Q&A
# ---------------------------
query = st.text_input("💬 Ask a question about Nairobi:")

if query:
    with st.spinner("🤔 Thinking..."):
        try:
            result = qa_chain.invoke(query)
            st.subheader("✅ Answer:")
            st.write(result["result"])

            st.subheader("📚 Sources:")
            for doc in result["source_documents"]:
                st.write(f"- {doc.metadata.get('source')}")
        except Exception as e:
            st.error(f"❌ Error while processing your question: {e}")
