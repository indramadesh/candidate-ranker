import faiss, numpy as np, os, json
from src.embed import embed_candidate_json

DATA_PROCESSED = os.path.join(os.getcwd(), "data", "processed")
INDEX_PATH = os.path.join(os.getcwd(), "outputs", "cand_index.faiss")
META_PATH = os.path.join(os.getcwd(), "outputs", "cand_meta.json")

def build_index():
    cand_files = [f for f in os.listdir(DATA_PROCESSED) if f.endswith(".json")]
    embeddings, ids = [], []
    for fname in cand_files:
        cid, emb = embed_candidate_json(os.path.join(DATA_PROCESSED, fname))
        embeddings.append(emb)
        ids.append(cid)
    embeddings = np.array(embeddings, dtype="float32")
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(ids, f)
    print(f"Indexed {len(ids)} candidates.")

if __name__ == "__main__":
    build_index()
