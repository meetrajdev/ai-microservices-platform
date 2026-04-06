from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import faiss
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Dummy documents (later replace with real docs)
documents = [
    "Kubernetes is used for container orchestration",
    "Spring Boot is used for building Java microservices",
    "RAG improves LLM responses using external data"
]

# Create embeddings
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Build FAISS index
embeddings = [get_embedding(doc) for doc in documents]
dimension = len(embeddings[0])
index = faiss.IndexFlatIP(dimension)
index.add(np.array(embeddings).astype(np.float32))


class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Hello AI Microservice"}

@app.post("/generate")
def generate_response(request: PromptRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request.prompt}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }

@app.post("/process")
def process_prompt(req):
    return {
        "processed_prompt": f"Refined: {req.prompt}"
    }

@app.post("/search")
def search(request: dict):
    query = request["query"]

    query_embedding = get_embedding(query)
    D, I = index.search(np.array([query_embedding]).astype("float32"), k=2)

    indices = vector_store.search(query_embedding)
    results = [documents[i] for i in np.indices[0]]

    results = [documents[i] for i in I[0]]

    return {
        "context": " ".join(results)
    }