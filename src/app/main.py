from fastapi import FastAPI

from app.apis import api_router

app = FastAPI(title="QA API")


app.include_router(api_router, prefix="/api")
