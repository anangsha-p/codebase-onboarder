import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import clone_repo, walk_files
from chunker import chunk_python_file

MODEL_NAME = "all-MiniLM-L6-v2"
DB_PATH = "chroma_db"

def build_index(repo_path, collection_name):
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=DB_PATH)

    # start fresh so re-running doesn't create duplicates
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    col = client.create_collection(collection_name)

    files = [f for f in walk_files(repo_path) if f["language"] == "python"]
    all_chunks = []
    for f in files:
        full = os.path.join(repo_path, f["path"])
        try:
            all_chunks.extend(chunk_python_file(full, display_path=f["path"]))
        except Exception as e:
            print(f"skipped {f['path']}: {e}")

    print(f"{len(files)} files -> {len(all_chunks)} chunks. Embedding...")

    BATCH = 64
    for i in range(0, len(all_chunks), BATCH):
        batch = all_chunks[i:i + BATCH]
        # put the name and path in the text so searches like "run method" can match
        texts = [f"{c['path']} {c['name']}\n{c['code']}" for c in batch]
        col.add(
            ids=[f"chunk_{i + j}" for j in range(len(batch))],
            documents=[c["code"] for c in batch],
            embeddings=model.encode(texts).tolist(),
            metadatas=[
                {"path": c["path"], "start": c["start"], "end": c["end"],
                 "name": c["name"], "kind": c["kind"], "language": c["language"]}
                for c in batch
            ],
        )
        print(f"  {min(i + BATCH, len(all_chunks))}/{len(all_chunks)}")
    print("Done.")

if __name__ == "__main__":
    repo_path = clone_repo(sys.argv[1])
    name = os.path.basename(repo_path)
    build_index(repo_path, name)