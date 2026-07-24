## Smart Resume Screening & Candidate Ranking Tool

A Streamlit Web application that screens and ranks candidate resumes against a job
description using TF-IDF keyword similarity (no external API needed) plus
a configurable skill-matching check.


## Features
- Upload multiple resumes at once: **PDF or DOCX**
- Paste any job description as plain text
- Ranks candidates by **TF-IDF cosine similarity** score (0–100%)
- Extracts and highlights **matched skills** per candidate 
- Best-effort extraction of **name, email, and phone number** from each resume
- Sortable results table, bar chart comparison, and per-candidate detail view
- **Download ranked results as CSV**
- Filters: minimum score threshold, top-N candidates

## Project structure
```
resume_screener/
├── app.py            # Streamlit UI - main entry point
├── resume_parser.py  # Text extraction (PDF/DOCX) + contact info
├── ranker.py          # TF-IDF vectorization, cosine similarity, skill matching
├── requirements.txt
└── README.md
```

## Setup

1. (Recommended) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Your browser will open at `http://localhost:8501`.

## How it works

1. **Parsing** (`resume_parser.py`): each uploaded file is converted to plain
   text using `PyPDF2` (PDF) or `python-docx` (DOCX). 
   A simple heuristic guesses the candidate's name from the first
   line of the resume (falls back to the filename), and regex patterns pull
   out an email address and phone number if present.

2. **Scoring** (`ranker.py`): the job description and every resume are
   combined into one corpus and vectorized with scikit-learn's
   `TfidfVectorizer` (unigrams + bigrams, English stop words removed). Each
   resume's **cosine similarity** to the job description becomes its match
   score (0–100%). Separately, a configurable list of skill keywords is
   checked against each resume's text with word-boundary regex matching, so
   you can see *why* a candidate scored the way they did.

3. **Ranking** (`app.py`): candidates are sorted by match score, filtered by
   your minimum score/top-N settings, and displayed in a table, a bar chart,
   and expandable detail cards — with a CSV export button.

## Customizing

- **Skill list**: edit the comma-separated list in the sidebar to match the
  role you're hiring for (e.g. add "figma", "salesforce", "gdpr").
- **Matching algorithm**: `ranker.py` is self-contained — swap in sentence
  embeddings (e.g. `sentence-transformers`) or an LLM-based semantic scorer
  later without touching the UI code, as long as you keep returning a
  0–100 `match_score` per candidate.
- **Contact extraction**: `resume_parser.py`'s regexes are intentionally
  simple; tighten or extend them if your resumes have a consistent format.

## Notes & limitations

- TF-IDF is a *keyword-overlap* method — it won't understand synonyms
  (e.g. "ML" vs. "machine learning") unless both phrasings appear somewhere
  in the corpus. For deeper semantic matching, consider upgrading to
  sentence embeddings.
- Scanned/image-only PDFs (no embedded text layer) won't extract any text;
  you'd need OCR (e.g. `pytesseract`) for those.
- Name/email/phone extraction is best-effort and may need manual review for
  unusually formatted resumes.
