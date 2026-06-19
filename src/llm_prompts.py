def candidate_summary_prompt(candidate_text: str, candidate_id: str) -> str:
    return f"""
You are an expert recruiter. Summarize the following candidate resume.

Candidate {candidate_id} Resume:
{candidate_text}

Output a JSON object with:
- candidate_id
- summary (short professional summary of skills, experience, and strengths)
- key_skills (list of top skills)
- experience_years (approximate years of experience)
- education (highest degree or qualification)

JSON only, no extra text.
"""
def candidate_ranking_prompt(job_description: str, candidate_summary: str, candidate_id: str) -> str:
    return f"""
You are an expert recruiter. Compare the following candidate summary against the job description.

Job Description:
{job_description}

Candidate {candidate_id} Summary:
{candidate_summary}

Output a JSON object with:
- candidate_id
- match_score (0–100)
- top_reasons (list of 3–5 reasons for the score)
- concerns (list of 2–3 weaknesses or gaps)

JSON only, no extra text.
"""
