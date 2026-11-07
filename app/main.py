from fastapi import FastAPI
from app.api.users import router as user_router

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def root():
    return {"msg": "bank is open"}