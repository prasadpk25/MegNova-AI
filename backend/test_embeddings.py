from App.ai.embeddings import generate_embedding

text = """
Hemoglobin: 13.5 g/dL
WBC: 7600 /uL
Platelets: 250000 /uL
Blood Sugar: 95 mg/dL
"""

embedding = generate_embedding(text)

print("Embedding length:", len(embedding))
print("First 10 values:")
print(embedding[:10])