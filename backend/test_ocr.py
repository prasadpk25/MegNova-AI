from App.ai.ocr import extract_text

image_path = "sample_report.png"

text = extract_text(image_path)

print("\n========== EXTRACTED TEXT ==========\n")
print(text)