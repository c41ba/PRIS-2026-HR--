from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence_avg: float | None


def _bytes_to_rgb_array(image_bytes: bytes) -> np.ndarray:
    """
    Decode image bytes into an RGB numpy array.
    Uses Pillow (installed as a dependency of Streamlit).
    """
    from PIL import Image  # pillow is typically present with streamlit

    with Image.open(io.BytesIO(image_bytes)) as im:
        im = im.convert("RGB")
        return np.array(im)


def extract_text_easyocr(
    image_bytes: bytes,
    *,
    languages: list[str] | None = None,
) -> OcrResult:
    """
    Week 7 — OCR module (EasyOCR)

    Accepts raw uploaded image bytes (e.g., from Streamlit file_uploader),
    extracts text using EasyOCR, and returns joined text + average confidence.
    """
    import io
    import easyocr

    if languages is None:
        languages = ["en"]

    rgb = _bytes_to_rgb_array(image_bytes)
    reader = easyocr.Reader(languages, gpu=False)
    results = reader.readtext(rgb)

    lines: list[str] = []
    confs: list[float] = []
    for _bbox, text, conf in results:
        t = str(text).strip()
        if t:
            lines.append(t)
        try:
            confs.append(float(conf))
        except Exception:
            pass

    joined = "\n".join(lines).strip()
    conf_avg: Optional[float] = (sum(confs) / len(confs)) if confs else None
    return OcrResult(text=joined, confidence_avg=conf_avg)


def ocr_then_extract_skills(
    image_bytes: bytes,
    *,
    languages: list[str] | None = None,
) -> dict[str, object]:
    """
    Convenience helper for the prototype:
    - OCR the resume image (Week 7)
    - Extract skills from OCR text (Week 6)
    """
    from weeks.week6_nlp import extract_skills_spacy

    ocr = extract_text_easyocr(image_bytes, languages=languages)
    skills = extract_skills_spacy(ocr.text).detected_skills
    return {
        "resume_text": ocr.text,
        "ocr_confidence_avg": ocr.confidence_avg,
        "detected_skills": skills,
    }


if __name__ == "__main__":
    # Manual test: point to a local image file.
    import pathlib
    import sys

    if len(sys.argv) < 2:
        print("Usage: python weeks/week7_cv.py path/to/resume_image.png")
        raise SystemExit(2)

    path = pathlib.Path(sys.argv[1])
    b = path.read_bytes()
    out = extract_text_easyocr(b)
    print("confidence_avg:", out.confidence_avg)
    print(out.text[:1000])

