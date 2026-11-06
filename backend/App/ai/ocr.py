
from pathlib import Path

import fitz
import easyocr
from docx import Document


# Load OCR model once
reader = easyocr.Reader(["en"])


def extract_text(file_path: str) -> str:
    """Extract text from PDF, DOCX and image reports."""

    path = Path(file_path)

    if not path.exists():
        return ""

    extension = path.suffix.lower()

    try:
        # PDF extraction
        if extension == ".pdf":
            with fitz.open(str(path)) as pdf:
                text = "\n".join(
                    page.get_text() for page in pdf
                ).strip()

            # Use OCR if PDF contains scanned pages
            if not text:
                with fitz.open(str(path)) as pdf:
                    for page in pdf:
                        pix = page.get_pixmap(dpi=200)
                        image_path = path.with_name(
                            f"{path.stem}_page.png"
                        )
                        pix.save(str(image_path))
                        text += "\n".join(
                            reader.readtext(
                                str(image_path), detail=0
                            )
                        ) + "\n"
                        image_path.unlink(missing_ok=True)

            return text.strip()

        # DOCX extraction
        elif extension == ".docx":
            document = Document(str(path))
            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

        # Image extraction
        elif extension in [".png", ".jpg", ".jpeg"]:
            result = reader.readtext(str(path), detail=0)
            return "\n".join(result).strip()

        return ""

    except Exception as error:
        print(f"Text extraction error: {error}")
        return ""
