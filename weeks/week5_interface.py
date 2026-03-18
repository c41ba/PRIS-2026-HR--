from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


SUPPORTED_SKILLS = [
    "Python",
    "SQL",
    "Java",
    "Docker",
    "Machine Learning",
    "Data Analysis",
]


@dataclass(frozen=True)
class Week5Inputs:
    job_description: str
    resume_text: str
    resume_image_bytes: Optional[bytes]
    resume_image_name: Optional[str]
    analyze_clicked: bool


def render_week5_app() -> Week5Inputs:
    """
    Week 5 — Basic Streamlit UI

    Collects:
    - Job description text
    - Resume text
    - Optional resume image upload
    - Analyze button click

    Week 5 only builds the UI and returns inputs. Full analysis is integrated in Week 9.
    """
    st.set_page_config(
        page_title="HR Assistant — AI Recruitment Tool",
        page_icon="🧑‍💼",
        layout="wide",
    )

    st.title("HR Assistant — AI Recruitment Tool")
    st.caption("Mid-term prototype (Weeks 3–10). Interface is introduced in Week 5.")

    with st.sidebar:
        st.header("Instructions")
        st.write(
            "1) Paste the **job description**.\n"
            "2) Paste **resume text** (or upload an image in later weeks).\n"
            "3) Click **Analyze Candidate** to run the prototype pipeline."
        )
        st.divider()
        st.subheader("Supported skills (prototype)")
        st.write(", ".join(SUPPORTED_SKILLS))

    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        st.subheader("Job description")
        job_description = st.text_area(
            label="Job description",
            placeholder="Paste the job description here…",
            height=180,
        )

        st.subheader("Resume text")
        resume_text = st.text_area(
            label="Resume text",
            placeholder="Paste the candidate resume text here…",
            height=220,
        )

    with col_right:
        st.subheader("Resume image (Week 7 OCR)")
        uploaded = st.file_uploader(
            "Upload resume image",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False,
        )

        analyze_clicked = st.button("Analyze Candidate", type="primary", use_container_width=True)

    resume_image_bytes = uploaded.getvalue() if uploaded is not None else None
    resume_image_name = uploaded.name if uploaded is not None else None

    st.divider()
    st.subheader("Results (Week 5 preview)")

    if analyze_clicked:
        st.info(
            "Week 5 builds the interface. Full analysis (OCR, NLP, rules, similarity) "
            "will be connected in Week 9."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Detected Skills", "—")
        c2.metric("Decision", "—")
        c3.metric("Similarity Score", "—")

        st.write("**Input summary**")
        st.table(
            [
                {
                    "job_description_chars": len(job_description or ""),
                    "resume_text_chars": len(resume_text or ""),
                    "resume_image_uploaded": bool(resume_image_bytes),
                    "resume_image_name": resume_image_name or "",
                }
            ]
        )
    else:
        st.write("Click **Analyze Candidate** to see results here.")

    return Week5Inputs(
        job_description=job_description,
        resume_text=resume_text,
        resume_image_bytes=resume_image_bytes,
        resume_image_name=resume_image_name,
        analyze_clicked=analyze_clicked,
    )

