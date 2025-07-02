from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

QDRANT_URL = ""  # Replace with your Qdrant server URL or whatever you have set up
COLLECTION = "pdf_qa"
MODEL_NAME = "all-MiniLM-L6-v2"  # open-source embedding or use Gemini model if you have access

qdrant = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer(MODEL_NAME)

server = FastMCP(name="Fetch Context", host="0.0.0.0", port=8050)


@server.tool()
async def fetch_context(query: str) -> list[dict] | None:
    """
    Fetch relevant context from the Qdrant vector database based on the user's query.
    This function encodes the query using a pre-trained model and retrieves the top matching points
    :param query: the user's query string to search for relevant context
    :return: The dict containing the top matching points with their IDs, text, and scores,
    """
    limit = 2
    qvec = model.encode(query)
    resp = qdrant.query_points(
        collection_name=COLLECTION,
        query=qvec,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )  # Replaces old `search()` now deprecated :contentReference[oaicite:2]{index=2}

    if not resp.points:
        return None
    return [{"id": p.id, "text": p.payload["text"], "score": p.score} for p in resp.points]

if __name__ == "__main__":
    server.run(transport="sse")
