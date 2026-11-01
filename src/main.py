import uvicorn
from fastapi import FastAPI
from database import Base, engine
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"msg": "bank is open"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir="src")