import os, json
from src.data_processing import load_raw_file, parse_resume_text

DATA_RAW = os.path.join(os.getcwd(), "data", "raw")
DATA_PROCESSED = os.path.join(os.getcwd(), "data", "processed")

def demo_parse():
    files = [f for f in os.listdir(DATA_RAW) if f.endswith(".txt")]
    for i, fname in enumerate(files[:5], start=1):
        path = os.path.join(DATA_RAW, fname)
        text = load_raw_file(path)
        parsed = parse_resume_text(text, candidate_id=f"cand_{i:03d}")
        print(f"Parsed {fname}: skills={parsed['skills']} companies={parsed['companies'][:2]}")
        # save JSON
        out_path = os.path.join(DATA_PROCESSED, f"{parsed['candidate_id']}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)

if __name__ == "__main__":
    demo_parse()
