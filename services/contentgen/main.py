from fastapi import FastAPI

app = FastAPI(title="contentgen Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "contentgen"}
