import os
import json

DATA_RANKING = "data/ranking"
DATA_OUTPUT = "data/output"

def aggregate_rankings(cutoff: int = 60):
    results = []

    # Load all ranking JSON files
    for fname in os.listdir(DATA_RANKING):
        path = os.path.join(DATA_RANKING, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            results.append(data)

    # Sort by match_score descending
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)

    # Save final ranked list
    os.makedirs(DATA_OUTPUT, exist_ok=True)
    out_path = os.path.join(DATA_OUTPUT, "final_ranked_candidates.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Split into matches vs rejections
    matches = [c for c in results if c["match_score"] >= cutoff]
    rejections = [c for c in results if c["match_score"] < cutoff]

    print(f"✅ Final ranked list saved to {out_path}")
    print(f"📊 Total Candidates: {len(results)}")
    print(f"✅ Matches (score ≥ {cutoff}): {len(matches)}")
    print(f"❌ Rejections (score < {cutoff}): {len(rejections)}")

    return results, matches, rejections

if __name__ == "__main__":
    aggregate_rankings()
