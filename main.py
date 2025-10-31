from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Your FastAPI server is running!"}
