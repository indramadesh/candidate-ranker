import os
import json
from src.ai_client import call_llm
from src.llm_prompts import candidate_ranking_prompt
from src.utils import load_raw_file, save_json_file

DATA_SUMMARY = "data/summary"
DATA_RANKING = "data/ranking"
DATA_JOB = "data/job"

def normalize_candidate_json(data: dict) -> dict:
    # Ensure top_reasons and concerns are lists, not dicts with numeric keys
    for key in ["top_reasons", "concerns"]:
        if isinstance(data.get(key), dict):
            data[key] = [v for _, v in sorted(data[key].items())]
    return data

def rank_candidates(job_file: str):
    job_description = load_raw_file(os.path.join(DATA_JOB, job_file))

    for fname in os.listdir(DATA_SUMMARY):
        candidate_id = fname.replace(".json", "")
        candidate_summary = load_raw_file(os.path.join(DATA_SUMMARY, fname))

        prompt = candidate_ranking_prompt(job_description, candidate_summary, candidate_id)
        ranking_text = call_llm(prompt)

        # Parse Gemini’s JSON output safely
        try:
            ranking_data = json.loads(ranking_text)
        except json.JSONDecodeError:
            cleaned = ranking_text.strip("```json").strip("```").strip()
            ranking_data = json.loads(cleaned)

        ranking_data = normalize_candidate_json(ranking_data)

        out_path = os.path.join(DATA_RANKING, f"{candidate_id}_rank.json")
        save_json_file(out_path, ranking_data)
        print(f"✅ Candidate {candidate_id} ranked → {out_path}")

if __name__ == "__main__":
    rank_candidates("job1.txt")
