from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ArticleInput(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "Your FastAPI server is running!"}

@app.post("/process")
def process_article(data: ArticleInput):
    # temporary testing response
    return {
        "received_url": data.url,
        "status": "OK"
    }
