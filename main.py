from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to your Affiliate Content Uploader API!"}

@app.get("/headline")
async def headline():
    return {
        "headline": "Maximize your earnings. Share. Promote. Profit.",
        "image_url": "/static/affiliate-banner.png",
        "tip": "Use this headline and image in your marketing materials to drive affiliate revenue."
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
