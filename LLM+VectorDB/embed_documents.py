import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Distance
from sentence_transformers import SentenceTransformer
import uuid

# Configuration
QDRANT_URL = ""  # Update with your Qdrant server URL or whatever you use
COLLECTION = "pdf_qa"
PDF_PATH = "path/to/your/document.pdf"  # Update with your PDF file path
MODEL_NAME = "all-MiniLM-L6-v2"  # Use gemini embedding model or any other embedding model you prefer

# Initialize Qdrant client
client = QdrantClient(url=QDRANT_URL)

# Delete the existing collection to remove old vectors
if client.collection_exists(COLLECTION):
    client.delete_collection(collection_name=COLLECTION)

# Create collection with the same vector configuration
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Load embedding model
model = SentenceTransformer(MODEL_NAME)

# Extract and chunk PDF with smaller chunks
with pdfplumber.open(PDF_PATH) as pdf:
    full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

# Updated smaller chunk size (e.g., 500) and chunk overlap (e.g., 100)
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=150)
chunks = splitter.split_text(full_text)

# Embed and prepare points
points = []
for text in chunks:
    vec = model.encode(text)
    points.append(PointStruct(id=uuid.uuid4().hex, vector=vec, payload={"text": text}))

# Upload to Qdrant
client.upsert(collection_name=COLLECTION, points=points, wait=True)
print(f"Indexed {len(points)} smaller chunks from the PDF.")