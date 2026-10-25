import os
import sys
from collections import Counter
from git import Repo

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".next"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "poetry.lock"}
EXT_TO_LANG = {".py": "python", ".js": "javascript", ".jsx": "javascript", ".ts": "typescript", ".md": "markdown", ".json": "json"}
MAX_SIZE = 1_000_000  # 1 MB

def clone_repo(url, dest="data"):
    name = url.rstrip("/").split("/")[-1].replace(".git", "")
    path = os.path.join(dest, name)
    if not os.path.exists(path):
        Repo.clone_from(url, path, depth=1)
    return path

def walk_files(repo_path):
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f in SKIP_FILES:
                continue
            full = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXT_TO_LANG or os.path.getsize(full) > MAX_SIZE:
                continue
            files.append({"path": os.path.relpath(full, repo_path), "language": EXT_TO_LANG[ext]})
    return files

if __name__ == "__main__":
    repo_path = clone_repo(sys.argv[1])
    files = walk_files(repo_path)
    stats = Counter(f["language"] for f in files)
    print(f"{len(files)} files found")
    for lang, count in stats.most_common():
        print(f"  {lang}: {count}")