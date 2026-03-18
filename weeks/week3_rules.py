from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class RuleDecision:
    decision: str  # "Accept" | "Reject"
    reasons: list[str]


def _normalize_skill_set(skills: Iterable[str]) -> set[str]:
    return {str(s).strip().lower() for s in skills if str(s).strip()}


def evaluate_candidate_rules(
    *,
    experience_years: float,
    candidate_skills: Iterable[str],
    required_skills: Iterable[str],
    min_experience_years: float = 1.0,
) -> RuleDecision:
    """
    Week 3 — Rule Engine

    Examples:
    - if experience < 1 year → Reject
    - if required skill missing → Reject
    - otherwise → Accept
    """
    reasons: list[str] = []

    if experience_years < min_experience_years:
        reasons.append(f"Experience below {min_experience_years} year(s).")

    candidate_set = _normalize_skill_set(candidate_skills)
    required_set = _normalize_skill_set(required_skills)

    missing = sorted(required_set - candidate_set)
    if missing:
        reasons.append("Missing required skill(s): " + ", ".join(missing))

    decision = "Reject" if reasons else "Accept"
    return RuleDecision(decision=decision, reasons=reasons)


def filter_candidates_by_rules(
    *,
    candidates: Iterable[Mapping[str, Any]],
    required_skills: Iterable[str],
    min_experience_years: float = 1.0,
) -> dict[str, list[dict[str, Any]]]:
    """
    Week 3 — Batch filtering helper.

    Each candidate mapping is expected to include:
    - "name" (optional, used for display)
    - "experience_years"
    - "skills" (iterable of strings)

    Returns:
      {"accepted": [...], "rejected": [...]}
    where each item includes the original candidate data plus "decision" and "reasons".
    """
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for c in candidates:
        exp = float(c.get("experience_years", 0.0))
        skills = c.get("skills", []) or []
        decision = evaluate_candidate_rules(
            experience_years=exp,
            candidate_skills=skills,
            required_skills=required_skills,
            min_experience_years=min_experience_years,
        )
        item = dict(c)
        item["decision"] = decision.decision
        item["reasons"] = decision.reasons

        (accepted if decision.decision == "Accept" else rejected).append(item)

    return {"accepted": accepted, "rejected": rejected}


if __name__ == "__main__":
    demo_candidates = [
        {"name": "Amina", "experience_years": 2, "skills": ["Python", "SQL", "Docker"]},
        {"name": "Ben", "experience_years": 0.5, "skills": ["Python"]},
        {"name": "Chao", "experience_years": 3, "skills": ["Java", "SQL"]},
    ]
    result = filter_candidates_by_rules(
        candidates=demo_candidates,
        required_skills=["Python", "SQL"],
        min_experience_years=1.0,
    )
    print(result)

