from fastapi import FastAPI

app = FastAPI(title="indexing Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "indexing"}
