import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

QDRANT_URL = ""
COLLECTION = "pdf_qa"
MODEL_NAME = "all-MiniLM-L6-v2"
LIMIT = 3


def fetch_context(query: str):
    model = SentenceTransformer(MODEL_NAME)
    qdrant = QdrantClient(url=QDRANT_URL)
    qvec = model.encode(query)
    resp = qdrant.query_points(
        collection_name=COLLECTION,
        query=qvec,
        limit=LIMIT,
        with_payload=True,
        with_vectors=False
    )
    if not resp.points:
        return None
    return [{"id": p.id, "text": p.payload["text"], "score": p.score} for p in resp.points]


def main():
    query = "What department does the author 'Atharva Jayappa' of the paper belong to at Vishwakarma Institute of Technology?"
    results = fetch_context(query)
    if results is None:
        print("No context found.")
    else:
        for i, r in enumerate(results, start=1):
            print(f"Result {i}:")
            print(f"\tid: {r['id']}")
            print(f"\ttext: {r['text']}")
            print(f"\tscore: {r['score']}")


if __name__ == "__main__":
    main()
