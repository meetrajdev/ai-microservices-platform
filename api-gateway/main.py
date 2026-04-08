from fastapi import FastAPI
import requests
import time

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Gateway running"}

def call_model_service(query):
    url = "http://model-service:8002/generate"

    for i in range(5):  # retry 5 times
        try:
            return requests.post(url, json=query).json()
        except Exception as e:
            print(f"Retry {i+1} failed:", e)
            time.sleep(2)

    raise Exception("Model service not available")


@app.post("/ask")
def ask(query: dict):
    return call_model_service(query)