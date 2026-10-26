import sys
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="chroma_db").get_collection(sys.argv[1])
q = model.encode([sys.argv[2]]).tolist()
res = col.query(query_embeddings=q, n_results=5)
for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
    print(f"{meta['path']}  {meta['name']}  lines {meta['start']}-{meta['end']}")