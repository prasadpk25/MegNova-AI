from sentence_transformers import SentenceTransformer
from App.qdrant_connection import client

COLLECTION_NAME = "clinical_guidelines"

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_guidelines(query, limit=5):
    query_text = query.strip()
    search_text = query_text

    # Domain-specific query expansion
    lower_query = query_text.lower()

    if (
        "hypertension" in lower_query
        and any(term in lower_query for term in [
            "first-line", "first line", "pharmacological",
            "medication", "drug", "treatment"
        ])
    ):
        search_text += (
            " thiazide and thiazide-like agents "
            "angiotensin converting enzyme inhibitors ACEi "
            "angiotensin receptor blockers ARB "
            "long-acting dihydropyridine calcium channel blockers CCB "
            "WHO initial antihypertensive treatment recommendation"
        )

    query_vector = model.encode(
        search_text,
        normalize_embeddings=True
    ).tolist()

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=20,
        with_payload=True,
        with_vectors=False,
    )

    candidates = []

    important_terms = [
        "thiazide",
        "angiotensin-converting enzyme",
        "angiotensin-receptor blockers",
        "long-acting dihydropyridine",
        "calcium channel blockers",
    ]

    for point in response.points:
        payload = point.payload or {}
        text = payload.get("text", "").strip()

        if not text:
            continue

        text_lower = text.lower()

        matches = sum(
            1 for term in important_terms
            if term in text_lower
        )

        candidates.append({
            "text": text,
            "score": point.score,
            "rank_score": point.score + (matches * 0.025),
        })

    candidates.sort(
        key=lambda item: item["rank_score"],
        reverse=True
    )

    return candidates[:limit]