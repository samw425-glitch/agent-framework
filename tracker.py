import json
import os

class UploaderTracker:
    """
    Tracker for uploaded files.
    """

    def __init__(self, config_path="config/uploader_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.upload_log = []

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"[Warning] Config file not found at {self.config_path}. Using defaults.")
            return {
                "upload_path": "/tmp/uploads",
                "allowed_extensions": ["jpg", "png", "gif"],
                "max_file_size_mb": 10
            }
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[Error] Invalid JSON in {self.config_path}. Using defaults.")
            return {
                "upload_path": "/tmp/uploads",
                "allowed_extensions": ["jpg", "png", "gif"],
                "max_file_size_mb": 10
            }

    def log_upload(self, filename, status="success"):
        self.upload_log.append({"filename": filename, "status": status})
        print(f"[Info] Upload logged: {filename} ({status})")

    def list_uploads(self):
        return self.upload_log
