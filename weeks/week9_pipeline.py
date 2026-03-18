from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from weeks.week3_rules import evaluate_candidate_rules
from weeks.week4_data_model import Candidate
from weeks.week6_nlp import SUPPORTED_SKILLS, extract_skills_spacy
from weeks.week7_cv import extract_text_easyocr
from weeks.week8_similarity import compute_tfidf_similarity


@dataclass(frozen=True)
class PipelineOutput:
    extracted_skills: list[str]
    decision: str
    similarity_score: float
    rule_reasons: list[str]
    used_ocr: bool
    ocr_confidence_avg: Optional[float]
    resume_text_final: str


def run_candidate_pipeline(
    *,
    job_description: str,
    resume_text_input: str,
    experience_years: float,
    resume_image_bytes: Optional[bytes] = None,
    required_skills: Iterable[str] = SUPPORTED_SKILLS,
) -> PipelineOutput:
    """
    Week 9–10 — Integration pipeline.

    Steps:
    1) If an image is provided, run OCR and treat its text as the resume text (overrides text box).
    2) Extract skills from the final resume text using spaCy.
    3) Apply rule-based decision on experience + extracted skills.
    4) Compute TF-IDF similarity between resume and job description.
    """
    used_ocr = False
    ocr_confidence_avg: Optional[float] = None
    resume_text_final = resume_text_input or ""

    if resume_image_bytes:
        ocr_res = extract_text_easyocr(resume_image_bytes)
        if ocr_res.text.strip():
            used_ocr = True
            resume_text_final = ocr_res.text
            ocr_confidence_avg = ocr_res.confidence_avg

    candidate = Candidate(
        name="Candidate",
        experience=experience_years,
        skills=[],
        resume_text=resume_text_final,
    )

    skill_result = extract_skills_spacy(candidate.resume_text)
    candidate.add_skills(skill_result.detected_skills)

    rule_decision = evaluate_candidate_rules(
        experience_years=candidate.experience,
        candidate_skills=candidate.skills,
        required_skills=required_skills,
        min_experience_years=1.0,
    )

    sim = compute_tfidf_similarity(
        resume_text=candidate.resume_text,
        job_description=job_description,
    )

    return PipelineOutput(
        extracted_skills=skill_result.detected_skills,
        decision=rule_decision.decision,
        similarity_score=sim.score,
        rule_reasons=rule_decision.reasons,
        used_ocr=used_ocr,
        ocr_confidence_avg=ocr_confidence_avg,
        resume_text_final=resume_text_final,
    )


if __name__ == "__main__":
    demo_job = "Looking for a Python developer with SQL, Docker and data analysis skills."
    demo_resume = "I am a Python developer with experience in SQL and Docker for data analysis."
    out = run_candidate_pipeline(
        job_description=demo_job,
        resume_text_input=demo_resume,
        experience_years=2.0,
        resume_image_bytes=None,
    )
    print(out)

