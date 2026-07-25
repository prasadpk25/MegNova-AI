from pathlib import Path

import easyocr


# Load OCR model once during application startup
reader = easyocr.Reader(["en"])


def extract_text(file_path: str) -> str:
    """
    Extract text from an image using EasyOCR.
    """

    path = Path(file_path)

    if not path.exists():
        return ""

    try:
        result = reader.readtext(str(path), detail=0)
        return "\n".join(result).strip()

    except Exception:
        return ""