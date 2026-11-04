import uvicorn
from fastapi import FastAPI
from api.users import router as user_router
from core.database import db_manager, Base

app = FastAPI()

app.include_router(user_router)

Base.metadata.create_all(bind=db_manager.engine)

@app.get("/")
async def root():
    return {"msg": "bank is open"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir="src")