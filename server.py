from mcp.server.fastmcp import FastMCP
import json
from difflib import get_close_matches

server = FastMCP(
    name="Fetch Context",
    host="0.0.0.0",
    port=8050
)


@server.tool()
async def fetch_context(query: str, cutoff: float = 0.6) -> dict | None:
    """
    Load MCP-server Q&A from the given JSON file,
    perform fuzzy matching on the questions,
    and return the best-matching QA pair.

    :param query:   The user's query string.
    :param cutoff:  Matching sensitivity (0.0–1.0); higher = stricter.
    :return:        The dict {"question": ..., "answer": ...} of the
                    best match, or None if no match exceeds the cutoff.
    """
    # Load all QA pairs
    with open("context.json", "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)

    # Extract question list for matching
    questions = [item["question"] for item in qa_pairs]

    # Fuzzy match: get the single best question
    matches = get_close_matches(query, questions, n=1, cutoff=cutoff)
    if not matches:
        return None

    best_question = matches[0]
    # Return the corresponding pair
    return next(pair for pair in qa_pairs if pair["question"] == best_question)


# Run the server
if __name__ == "__main__":
    try:
        server.run(transport="sse")
    except KeyboardInterrupt:
        print("Server stopped by user.")
