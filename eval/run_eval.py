import json
import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION = "flask"
K = 5

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="chroma_db").get_collection(COLLECTION)

with open("eval/questions.json", encoding="utf-8") as f:
    questions = json.load(f)

hits = 0
for item in questions:
    q = model.encode([item["question"]]).tolist()
    res = col.query(query_embeddings=q, n_results=K)
    files = [m["path"].replace("\\", "/") for m in res["metadatas"][0]]
    ok = any(item["file"] in p for p in files)
    hits += ok
    print(("PASS" if ok else "FAIL"), "|", item["question"])
    if not ok:
        print("      got:", files)

print(f"\nTop-{K} accuracy: {hits}/{len(questions)} = {hits / len(questions):.0%}")