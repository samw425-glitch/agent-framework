from fastapi import FastAPI

app = FastAPI(title="analytics Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "analytics"}
