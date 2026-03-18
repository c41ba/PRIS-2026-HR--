# HR Assistant (Recruitment Helper) — Mid-term Prototype (Weeks 3–10)

This project is a university prototype for the course **Design and Development of Intelligent Systems**.  
It implements functionality **only up to Weeks 9–10 (Mid-term prototype)**.

## What it demonstrates

- Rule-based filtering (Week 3)
- Candidate data model (Week 4)
- Streamlit UI (Week 5)
- NLP skill extraction with spaCy (Week 6)
- OCR resume text extraction with EasyOCR (Week 7)
- Similarity search with TF-IDF + cosine similarity (Week 8)
- Integrated pipeline connecting all modules (Weeks 9–10)

## Project structure

```
hr_assistant/
weeks/
  week3_rules.py
  week4_data_model.py
  week5_interface.py
  week6_nlp.py
  week7_cv.py
  week8_similarity.py
  week9_pipeline.py
ui/
  app.py
modules/
  __init__.py
data/
requirements.txt
README.md
```

## Install

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run

```bash
streamlit run ui/app.py
```

## Notes / limitations (by course requirement)

- No authentication
- No backend REST API
- No database
- No deployment
- No advanced ML training (Weeks 11–15 are intentionally not implemented)

