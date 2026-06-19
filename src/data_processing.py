import spacy
import re
import csv
import os
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

# Load skill map
def load_skill_map(path="data/skills_map.csv") -> Dict[str, str]:
    mapping = {}
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row["keyword"].lower()] = row["canonical"]
    return mapping

skill_map = load_skill_map()

def normalize_skill(skill: str) -> str:
    return skill_map.get(skill.lower(), skill)

def extract_entities(text: str) -> Dict:
    doc = nlp(text)
    companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    dates = [ent.text for ent in doc.ents if ent.label_ in ["DATE"]]
    skills = []
    # crude regex for skills (expand later)
    for token in doc:
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            if token.text.lower() in skill_map:
                skills.append(normalize_skill(token.text))
    return {"companies": companies, "dates": dates, "skills": list(set(skills))}

def parse_resume_text(text: str, candidate_id: str = None) -> Dict:
    entities = extract_entities(text)
    return {
        "candidate_id": candidate_id or "unknown",
        "raw_text": text[:1000],
        "companies": entities["companies"],
        "dates": entities["dates"],
        "skills": entities["skills"]
    }

def load_raw_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
