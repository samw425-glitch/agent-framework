from fastapi import FastAPI

app = FastAPI(title="backlinking Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "backlinking"}
