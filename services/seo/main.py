from fastapi import FastAPI

app = FastAPI(title="seo Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "seo"}
