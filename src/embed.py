from sentence_transformers import SentenceTransformer
import os, json

# load model once
model = SentenceTransformer("all-mpnet-base-v2")

def embed_text(text: str):
    """Return normalized embedding vector for given text."""
    return model.encode([text], normalize_embeddings=True)[0]

def embed_candidate_json(path: str):
    """Load candidate JSON and embed relevant fields."""
    with open(path, "r", encoding="utf-8") as f:
        cand = json.load(f)
    text = " ".join([
        cand.get("raw_text", ""),
        " ".join(cand.get("skills", [])),
        " ".join(cand.get("companies", []))
    ])
    return cand["candidate_id"], embed_text(text)

def embed_job_text(job_text: str):
    """Embed job description text."""
    return embed_text(job_text)

