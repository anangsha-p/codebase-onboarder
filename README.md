# 🧭 Codebase Onboarder AI

**An AI-powered tool that helps developers understand unfamiliar GitHub repositories through natural-language questions and source-code references.**

Codebase Onboarder AI uses Retrieval-Augmented Generation (RAG) to analyze repository code, retrieve relevant information, and generate context-aware explanations with file and line references.

## 🚀 Features

- **GitHub Repository Management:** Add and manage repositories for code exploration.
- **Automated Code Analysis:** Processes repository files and identifies important code components.
- **AI-Powered Code Assistant:** Ask questions about the selected codebase in natural language.
- **Intelligent Code Retrieval:** Finds relevant code sections based on user queries.
- **Source-Based Answers:** Provides file references and line numbers to help verify responses.
- **Repository Overview:** Helps users understand the structure and architecture of a codebase.
- **User Authentication:** Provides a login system for accessing the application.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | User interface |
| GitPython | Repository handling |
| Tree-sitter | Code parsing |
| Sentence Transformers | Code embeddings |
| ChromaDB | Vector storage and retrieval |
| Google Gemini API | AI-generated explanations |
| Google OAuth | User authentication |

## ⚙️ How It Works

1. User signs in and selects a GitHub repository.
2. The system retrieves and processes the repository files.
3. Code is divided into meaningful chunks and converted into embeddings.
4. Relevant code sections are retrieved based on the user's question.
5. Gemini generates an explanation using the retrieved context.
6. The application displays the answer with supporting source references.

## 💻 Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/anangsha-p/codebase-onboarder.git
cd codebase-onboarder
```

Create and activate a virtual environment:

```bash
py -3.14 -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required API credentials and authentication settings, then run:

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 📊 Project Status

- [x] Initial project setup
- [x] Repository ingestion
- [x] Code parsing and chunking
- [x] Embedding generation and vector indexing
- [x] AI-powered question answering
- [x] Source-based answer references
- [x] Repository overview
- [x] User interface and authentication
- [x] Initial functional testing

## 🔮 Future Improvements

- Advanced code dependency visualization
- Personalized developer onboarding paths
- Support for additional programming languages
- Improved retrieval accuracy and evaluation

## 👩‍💻 Developer

**Anangsha Pal**  
B.Tech Computer Science and Engineering  
Institute of Engineering and Management, Kolkata

---

*Making code exploration smarter, faster, and simpler.*