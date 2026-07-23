import fitz
from pathlib import Path

def load_guidelines(folder_path: str):
    documents = []

    folder = Path(folder_path)

    for pdf_file in folder.rglob("*.pdf"):
        try:
            print(f"Loading: {pdf_file}")

            doc = fitz.open(pdf_file)

            text = ""
            for page in doc:
                text += page.get_text()

            doc.close()

            documents.append({
                "file_name": pdf_file.name,
                "text": text
            })

        except Exception as e:
            print(f"Skipped {pdf_file.name}: {e}")

    return documents