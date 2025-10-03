from fastapi import FastAPI
from routes import router

app = FastAPI(title="Multi-Uploader API")
app.include_router(router)
