## Smart Resume Screening & Candidate Ranking Tool

A Streamlit Web application that screens and ranks candidate resumes against a job
description using TF-IDF keyword similarity and a configurable skill-matching check 
without any external API.



## Features

- Upload multiple resumes at once: **PDF or DOCX**
- Paste any job description as plain text
- Ranks candidates by **TF-IDF cosine similarity** score (0–100%)
- Extracts and highlights **matched skills** per candidate 
- Extracts **name, email, and phone number** from each resume
- Sorts results table, bar chart comparison, and per-candidate detail view
- Filters: minimum score threshold, top-N candidates



## Project structure

- resume_screening_app.py     # Streamlit UI
- resume_parser.py            # Text extraction (PDF+DOCS) & Contact Info
- ranker.py                   # TF-IDF vectorization, cosine similarity & skill matching
- requirements.txt
- Readme.md



## Working

1. **Parsing** (`resume_parser.py`): each uploaded file is converted to plain
   text using `PyPDF2` (PDF) or `python-docx` (DOCX). 

2. **Scoring** (`ranker.py`): the job description and every resume are
   combined into one corpus and vectorized with scikit-learn's
   `TfidfVectorizer`. Each resume's **cosine similarity** to the job 
   description becomes its match score (0–100%).
   
4. **Ranking** (`resume_screening_app.py`): candidates are sorted by match score, filtered by
   your minimum score/top-N settings, and displayed in a table, a bar chart,
   and expandable details.



## Notes & limitations

- TF-IDF doesn't understand synonyms
  (e.g. "ML" vs. "machine learning") unless both phrasings appear somewhere
  in the corpus.
  
- Scanned/image-only PDFs won't extract any text without OCR.
  
- Name/email/phone extraction is best-effort and may need manual review for
  unusually formatted resumes.



