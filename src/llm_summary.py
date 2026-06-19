import os
from src.ai_client import call_llm
from src.llm_prompts import candidate_summary_prompt
from src.utils import load_raw_file, save_json_file

DATA_RAW = "data/raw"
DATA_SUMMARY = "data/summary"

def summarize_candidate(fname: str, candidate_id: str):
    text = load_raw_file(os.path.join(DATA_RAW, fname))
    prompt = candidate_summary_prompt(text, candidate_id)
    summary_text = call_llm(prompt)

    # Save summary JSON
    out_path = os.path.join(DATA_SUMMARY, f"{candidate_id}.json")
    save_json_file(out_path, summary_text)
    print(f"✅ Candidate {candidate_id} summary saved to {out_path}")
