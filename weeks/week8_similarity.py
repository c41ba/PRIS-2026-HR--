from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class SimilarityResult:
    score: float  # 0.0–1.0


def compute_tfidf_similarity(
    resume_text: str,
    job_description: str,
) -> SimilarityResult:
    """
    Week 8 — TF-IDF + cosine similarity.

    Returns a similarity score in the range [0, 1].
    """
    texts = [resume_text or "", job_description or ""]

    if not any(t.strip() for t in texts):
        return SimilarityResult(score=0.0)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = float(sim_matrix[0, 0])

    # Clip for numerical stability.
    if score < 0.0:
        score = 0.0
    elif score > 1.0:
        score = 1.0

    return SimilarityResult(score=score)


if __name__ == "__main__":
    r = "Python developer with experience in data analysis and machine learning."
    j = "We are looking for a Python engineer skilled in data analysis and ML."
    res = compute_tfidf_similarity(r, j)
    print("similarity:", round(res.score, 3))

