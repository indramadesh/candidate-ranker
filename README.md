# Candidate Ranker

An AI-powered app to rank job candidates against a job description using Gemini LLM.

## Features
- Upload job description (file or link)
- Upload multiple resumes
- Rank candidates with match scores
- Show top reasons and concerns
- Interactive cutoff slider in Streamlit

## Quick Start (Windows)
1. python -m venv .venv
2. .venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. Add sample resumes to data\raw
5. Run: .venv\Scripts\python.exe src\main.py

## Setup
```bash
git clone https://github.com/indramadesh/candidate-ranker.git
cd candidate-ranker
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
