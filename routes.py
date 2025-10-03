from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from tracker import UploaderTracker

router = APIRouter()
tracker = UploaderTracker()

os.makedirs(tracker.config["upload_path"], exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    if ext not in tracker.config["allowed_extensions"]:
        tracker.log_upload(filename, status="rejected")
        raise HTTPException(status_code=400, detail=f"File type .{ext} not allowed.")

    upload_path = os.path.join(tracker.config["upload_path"], filename)

    with open(upload_path, "wb") as f:
        content = await file.read()
        if len(content) > tracker.config["max_file_size_mb"] * 1024 * 1024:
            tracker.log_upload(filename, status="rejected")
            raise HTTPException(status_code=400, detail="File too large.")
        f.write(content)

    tracker.log_upload(filename)
    return {"filename": filename, "status": "success"}

@router.get("/uploads")
def list_uploads():
    return tracker.list_uploads()
