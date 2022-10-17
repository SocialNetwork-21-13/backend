from fastapi import FastAPI
import uvicorn
import gridfs
from dotenv import dotenv_values
from pymongo import MongoClient
from endpoints.user import router as user_router
from endpoints.auth import router as auth_router

config = dotenv_values(".env")

app = FastAPI(title="Ryglogram")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)

app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])