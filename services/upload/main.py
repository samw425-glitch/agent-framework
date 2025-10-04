from fastapi import FastAPI

app = FastAPI(title="upload Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "upload"}
