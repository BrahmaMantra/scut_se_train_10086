from fastapi import FastAPI
import src.api as api

app = FastAPI()

app.include_router(router=api.v1_router, prefix="/v1")


@app.get("/ping")
def ping():
    return {"message": "pong"}
