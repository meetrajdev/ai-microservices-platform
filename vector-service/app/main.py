from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
import numpy as np
import os
import faiss
from dotenv import load_dotenv
from app.faiss_store import FAISSStore
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

documents = []
index = None
vector_store = None

class QueryRequest(BaseModel):
    query: str

class IngestRequest(BaseModel):
    documents: list[str]

# Embedding function
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Create embedding
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Ingest

@app.post("/ingest")
def ingest():
    global index, documents

    documents = [
        "Kubernetes is used for container orchestration",
        "Spring Boot is used for building Java microservices",
        "RAG improves LLM responses using external data"
    ]

    embeddings = [get_embedding(doc) for doc in documents]

    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)

    index.add(np.array(embeddings).astype("float32"))

    return {"message": "Documents ingested"}

# Search
@app.post("/search")
def search(request: dict):
    global index, documents

    if index is None:
        return {"error": "No data ingested yet"}

    query = request["query"]
    query_embedding = get_embedding(query)

    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        k=2
    )

    results = [documents[i] for i in I[0]]

    return {
        "context": " ".join(results)
    }