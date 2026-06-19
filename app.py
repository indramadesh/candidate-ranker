import os
import json
import streamlit as st
from src.llm_rank import rank_candidates
from src.llm_aggregate import aggregate_rankings

DATA_OUTPUT = "data/output"
DATA_RAW = "data/raw"

def normalize_candidate_json(data: dict) -> dict:
    # Ensure top_reasons and concerns are lists, not dicts with numeric keys
    for key in ["top_reasons", "concerns"]:
        if isinstance(data.get(key), dict):
            data[key] = [v for _, v in sorted(data[key].items())]
    return data

def load_results():
    out_path = os.path.join(DATA_OUTPUT, "final_ranked_candidates.json")
    if not os.path.exists(out_path):
        return []
    with open(out_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    return [normalize_candidate_json(c) for c in results]

# Streamlit UI
st.title("AI Candidate Ranker")

# --- Job Description Input ---
jd_option = st.radio("Provide Job Description:", ["Upload File", "Paste Link"])
if jd_option == "Upload File":
    jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
    if jd_file:
        os.makedirs("data/job", exist_ok=True)
        with open("data/job/job1.txt", "wb") as f:
            f.write(jd_file.getbuffer())
        st.success("Job description uploaded successfully!")
elif jd_option == "Paste Link":
    jd_link = st.text_input("Paste Job Posting Link")
    if jd_link:
        import requests
        from bs4 import BeautifulSoup
        try:
            response = requests.get(jd_link)
            soup = BeautifulSoup(response.text, "html.parser")
            job_text = soup.get_text(separator="\n")
            os.makedirs("data/job", exist_ok=True)
            with open("data/job/job1.txt", "w", encoding="utf-8") as f:
                f.write(job_text)
            st.success("Job description fetched and saved!")
        except Exception as e:
            st.error(f"Failed to fetch job description: {e}")  # ✅ fixed line

# --- Resume Upload Section ---
resume_files = st.file_uploader("Upload Candidate Resumes (.txt)", type=["txt"], accept_multiple_files=True)
if resume_files:
    os.makedirs(DATA_RAW, exist_ok=True)
    for resume in resume_files:
        resume_path = os.path.join(DATA_RAW, resume.name)
        with open(resume_path, "wb") as f:
            f.write(resume.getbuffer())
    st.success(f"{len(resume_files)} resumes uploaded successfully!")

# --- Candidate Ranking Button ---
if st.button("Rank Candidates"):
    rank_candidates("job1.txt")
    results, matches, rejections = aggregate_rankings()
    st.success("Ranking complete!")

    # Show totals
    st.subheader("Summary")
    st.write(f"📊 Total Candidates: {len(results)}")
    st.write(f"✅ Matches (score ≥ 60): {len(matches)}")
    st.write(f"❌ Rejections (score < 60): {len(rejections)}")

    # Interactive cutoff slider
    cutoff = st.slider("Set cutoff score for matches", 50, 80, 60)
    matches = [c for c in results if c["match_score"] >= cutoff]
    rejections = [c for c in results if c["match_score"] < cutoff]

    st.subheader("Top Matches")
    for cand in matches:
        st.write(f"**Candidate ID:** {cand['candidate_id']}")
        st.write(f"**Match Score:** {cand['match_score']}")
        st.write("**Top Reasons:**")
        for reason in cand['top_reasons']:
            st.write(f"- {reason}")
        st.write("**Concerns:**")
        for concern in cand['concerns']:
            st.write(f"- {concern}")
        st.markdown("---")

    st.subheader("Rejected Candidates")
    for cand in rejections:
        st.write(f"**Candidate ID:** {cand['candidate_id']}")
        st.write(f"**Match Score:** {cand['match_score']}")
        st.write("**Top Reasons:**")
        for reason in cand['top_reasons']:
            st.write(f"- {reason}")
        st.write("**Concerns:**")
        for concern in cand['concerns']:
            st.write(f"- {concern}")
        st.markdown("---")
