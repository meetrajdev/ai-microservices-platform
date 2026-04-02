from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    question: str

@app.post("/generate")
def generate_response(req: Request):
    question = req.question
    
    # Dummy AI logic for now
    return f"AI response to: {question}"