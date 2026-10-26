import os
import sys
import chromadb
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
TOP_K = 6

embedder = SentenceTransformer("all-MiniLM-L6-v2")
llm = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def retrieve(collection_name, question, k=TOP_K):
    col = chromadb.PersistentClient(path="chroma_db").get_collection(collection_name)
    q = embedder.encode([question]).tolist()
    res = col.query(query_embeddings=q, n_results=k)
    return list(zip(res["documents"][0], res["metadatas"][0]))

def build_prompt(question, chunks):
    context = ""
    for code, m in chunks:
        context += f"File: {m['path']} (lines {m['start']}-{m['end']}) [{m['name']}]\n{code}\n\n---\n\n"
    return f"""You are a helpful assistant that helps new developers understand a codebase.
Answer the question using ONLY the code below.
Cite the file path and line numbers for every claim, like (app.py, lines 630-689).
If the answer is not in the code below, say "I could not find this in the retrieved code."

CODE:
{context}
QUESTION: {question}
"""

def answer(collection_name, question):
    chunks = retrieve(collection_name, question)
    prompt = build_prompt(question, chunks)
    r = llm.models.generate_content(model=MODEL, contents=prompt)
    return r.text, chunks

if __name__ == "__main__":
    text, chunks = answer(sys.argv[1], sys.argv[2])
    print(text)
    print("\nSources:")
    for _, m in chunks:
        print(f"  {m['path']}  {m['name']}  lines {m['start']}-{m['end']}")