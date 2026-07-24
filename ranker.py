"""

Scores and Ranks Resumes

"""


import re 
from typing import List, Dict


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "r", "html", "css", 
    "react", "angular", "node.js", "django", "flask", "git", "machine learning", "deeplearning",
    "vue", "azure", "aws", "gcp", "docker", "kubernetes", "rest api", "agile", "scrum",
    "nlp", "data analysis", "data science", "pandas", "numpy", "scikit-learn", "tensorflow", 
    "pytorch", "tableau", "power bi", "excel", "linux", "pcb", "vlsi", "iot","microcontrollers", 
    "microprocessors", "control systems", "circuit design", "matlab", "ltspice", "arduino ide", 
    "xilinx", "soft skills", "project management", "communication", "leadership" 
    ]


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_similarity_scores(job_description: str, resume_texts: List[str]) -> List[float]:

    corpus = [clean_text(job_description)] + [clean_text(t) for t in resume_texts]

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(corpus)

    job_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(job_vector, resume_vectors)[0]
    return [round(float(score) * 100, 2) for score in similarities]


def extract_matched_skills(text: str, skills: List[str]) -> List[str]:
    lower_text = text.lower()
    matched = []
    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, lower_text):
            matched.append(skill)
    return matched


def rank_candidates(
    job_description: str,
    candidates: List[Dict],
    skills: List[str] = None,
) -> List[Dict]:
    
    if skills is None:
        skills = DEFAULT_SKILLS

    texts = [c["text"] for c in candidates]
    scores = compute_similarity_scores(job_description, texts)

    for candidate, score in zip(candidates, scores):
        candidate["match_score"] = score
        matched = extract_matched_skills(candidate["text"], skills)
        candidate["matched_skills"] = matched
        candidate["skill_count"] = len(matched)

    ranked = sorted(candidates, key=lambda c: c["match_score"], reverse=True)
    return ranked


