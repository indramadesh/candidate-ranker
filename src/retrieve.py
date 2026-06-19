import faiss, numpy as np, json, os
from src.embed import embed_job_text

INDEX_PATH = os.path.join(os.getcwd(), "outputs", "cand_index.faiss")
META_PATH = os.path.join(os.getcwd(), "outputs", "cand_meta.json")

def retrieve_candidates(job_text: str, k=10):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        ids = json.load(f)
    job_emb = embed_job_text(job_text).astype("float32")
    job_emb = np.expand_dims(job_emb, axis=0)
    D, I = index.search(job_emb, k)
    results = [(ids[i], float(D[0][j])) for j, i in enumerate(I[0])]
    return results

if __name__ == "__main__":
    jd = "Senior backend engineer with Python and distributed systems experience."
    top = retrieve_candidates(jd, k=5)
    print("Top candidates:", top)
