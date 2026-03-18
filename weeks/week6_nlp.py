from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import spacy
from spacy.language import Language
from spacy.matcher import PhraseMatcher


SUPPORTED_SKILLS = [
    "Python",
    "SQL",
    "Java",
    "Docker",
    "Machine Learning",
    "Data Analysis",
]


@dataclass(frozen=True)
class SkillExtractionResult:
    detected_skills: list[str]


def load_spacy_pipeline(model_name: str = "en_core_web_sm") -> Language:
    """
    Week 6 — spaCy pipeline loader.

    Tries to load a real English model. If it's not installed yet,
    falls back to a blank English pipeline so the prototype remains runnable.
    """
    try:
        return spacy.load(model_name)
    except Exception:
        # Fallback keeps tokenization; NER/lemmatizer aren't required for phrase matching.
        return spacy.blank("en")


def extract_skills_spacy(
    text: str,
    *,
    nlp: Language | None = None,
    skills: Iterable[str] = SUPPORTED_SKILLS,
) -> SkillExtractionResult:
    """
    Week 6 — NLP skill extraction using spaCy.

    Uses PhraseMatcher to detect occurrences of supported skills in the resume text.
    Returns canonical skill names (e.g., "Machine Learning") with duplicates removed.
    """
    if nlp is None:
        nlp = load_spacy_pipeline()

    doc = nlp(text or "")

    skill_list = [str(s).strip() for s in skills if str(s).strip()]
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(s) for s in skill_list]
    matcher.add("SKILLS", patterns)

    matches = matcher(doc)
    found_lower: set[str] = set()
    for _match_id, start, end in matches:
        span_text = doc[start:end].text.strip().lower()
        if span_text:
            found_lower.add(span_text)

    # Map back to canonical names and keep stable ordering.
    canonical_by_lower = {s.lower(): s for s in skill_list}
    detected = [canonical_by_lower[s.lower()] for s in skill_list if s.lower() in found_lower]

    return SkillExtractionResult(detected_skills=detected)


if __name__ == "__main__":
    sample = (
        "Data analyst with strong Python and SQL skills. "
        "Built Dockerized pipelines for machine learning projects."
    )
    res = extract_skills_spacy(sample)
    print(res.detected_skills)

