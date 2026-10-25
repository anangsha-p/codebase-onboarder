from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
col = client.create_collection("test")

docs = [
    "def login(user, pw): check password",
    "def draw_chart(data): plot bars",
    "def logout(user): end session",
]
col.add(ids=["1", "2", "3"], documents=docs, embeddings=model.encode(docs).tolist())

q = model.encode(["how does authentication work?"]).tolist()
print(col.query(query_embeddings=q, n_results=1)["documents"])