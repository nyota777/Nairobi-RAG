# 🌍 Nairobi-RAG Chatbot  

An **AI-powered Retrieval-Augmented Generation (RAG) chatbot** about **Nairobi City, its History, National Park, and Museums**.  

Built with **Streamlit, LangChain, FAISS, HuggingFace embeddings, and Gemini (Google Generative AI)**, this chatbot retrieves knowledge from curated sources and generates **context-aware answers with citations**.  

---
## ⚙️ Installation  

### 1. Clone the repository  
```bash
git clone https://github.com/<your-username>/Nairobi-RAG.git
cd Nairobi-RAG
2. Create a virtual environment
bash
Copy code
python -m venv .venv
Activate it:

Windows (PowerShell):

bash
Copy code
.venv\Scripts\activate
Mac/Linux:

bash
Copy code
source .venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file in the project root and add your API key:

ini
Copy code
GOOGLE_API_KEY=your_gemini_api_key
👉 Get your Gemini API key here: Google AI Studio

📦 requirements.txt
Here’s a sample requirements.txt you can use:

txt
Copy code
streamlit
python-dotenv
langchain
langchain-google-genai
langchain-community
faiss-cpu
huggingface-hub
sentence-transformers
pillow
🚀 Running the App
Start the Streamlit app:

bash
Copy code
streamlit run app.py
Then open the URL shown in your terminal (usually http://localhost:8501)

📚 How It Works
Embeddings → Source documents in /data/ are converted into vector embeddings using HuggingFace models.

Vector Store → FAISS stores and retrieves the most relevant chunks.

LLM (Gemini) → Gemini generates context-aware answers.

Streamlit UI → Users can interact with the chatbot via a web interface.

📌 Adding New Data
Place your PDFs, transcripts, or text files in the data/ folder.

Run your indexing script (to embed & store data in FAISS).
Example (pseudo):

bash
Copy code
python build_index.py
Restart the app:

bash
Copy code
streamlit run app.py
🎯 Future Improvements
✅ Add more Nairobi-related datasets (tourism blogs, government resources).

✅ Support multilingual Q&A (Swahili + English).

✅ Deploy on Streamlit Cloud or Hugging Face Spaces.

📜 License
This project is open-source under the MIT License.

👨‍💻 Author
Developed by Arthur Nyota
Email nyotaarthur345@gmail.com

yaml
Copy code
