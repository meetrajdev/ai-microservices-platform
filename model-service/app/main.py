
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Model Service Running"}

@app.post("/generate")
def generate_response(request: PromptRequest):
    question = request.prompt

    # Step 1: Call vector-service
    search_response = requests.post(
        "http://vector-service:8001/search",
        json={"query": question}
    )

    context = search_response.json().get("context", "")

    # Step 2: Send context + question to LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Use this context to answer:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "context_used": context
    }