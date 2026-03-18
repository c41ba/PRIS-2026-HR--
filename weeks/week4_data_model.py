from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


def _normalize_skill(s: str) -> str:
    return str(s).strip().lower()


@dataclass
class Candidate:
    """
    Week 4 — Data model

    Minimal candidate representation for the mid-term prototype (Weeks 3–10).
    """

    name: str
    experience: float  # years
    skills: list[str] = field(default_factory=list)
    resume_text: str = ""

    def normalized_skills(self) -> set[str]:
        return {_normalize_skill(s) for s in self.skills if _normalize_skill(s)}

    def add_skills(self, new_skills: Iterable[str]) -> None:
        for s in new_skills:
            s_norm = str(s).strip()
            if not s_norm:
                continue
            self.skills.append(s_norm)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "experience": self.experience,
            "skills": list(self.skills),
            "resume_text": self.resume_text,
        }


if __name__ == "__main__":
    c = Candidate(
        name="Demo Candidate",
        experience=2.5,
        skills=["Python", "SQL"],
        resume_text="Experienced in Python and SQL, plus some Docker.",
    )
    c.add_skills(["Docker", "  ", "Machine Learning"])
    print(c.to_dict())
    print("normalized_skills:", sorted(c.normalized_skills()))
