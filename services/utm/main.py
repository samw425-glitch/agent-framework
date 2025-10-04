from fastapi import FastAPI

app = FastAPI(title="utm Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "utm"}
