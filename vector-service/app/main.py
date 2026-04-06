from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv
from app.faiss_store import FAISSStore

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

documents = []
vector_store = None

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

# Ingest
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    chunks = text.split("\n")

    embeddings = []

    for chunk in chunks:
        if chunk.strip():
            documents.append(chunk)
            embeddings.append(get_embedding(chunk))

    global vector_store

    if vector_store is None:
        vector_store = FAISSStore(len(embeddings[0]))

    vector_store.add(embeddings)

    return {"message": "Ingested", "chunks": len(embeddings)}

# Search
@app.post("/search")
def search(request: dict):
    query = request["query"]

    query_embedding = get_embedding(query)

    indices = vector_store.search(query_embedding)

    results = [documents[i] for i in indices[0]]

    return {
        "context": " ".join(results)
    }