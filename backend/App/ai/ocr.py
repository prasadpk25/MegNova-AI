import easyocr

# Load OCR model once
reader = easyocr.Reader(["en"])


def extract_text(image_path: str):
    """
    Extract text from an image.
    """

    result = reader.readtext(image_path, detail=0)

    return "\n".join(result)