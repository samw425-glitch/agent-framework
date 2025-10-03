import time
import random
from typing import List

class Uploader:
    def __init__(self, name: str, base_url: str, api_keys: List[str]):
        self.name = name
        self.base_url = base_url
        self.api_keys = api_keys
        self.current_key_index = 0

    def get_next_key(self) -> str:
        """Rotate API keys in round-robin fashion"""
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
