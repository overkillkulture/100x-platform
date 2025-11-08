"""MODULE #39: FILE STORAGE - Cloud-style file storage"""
import os
import json
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class FileMetadata:
    id: str
    filename: str
    size: int
    hash: str
    created: float
    tags: List[str]

class FileStorage:
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = storage_path
        self.metadata_path = os.path.join(storage_path, "metadata.json")
        self.files: Dict[str, FileMetadata] = {}
        os.makedirs(storage_path, exist_ok=True)
        self._load_metadata()

    def _load_metadata(self):
        """Load file metadata"""
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                data = json.load(f)
                self.files = {k: FileMetadata(**v) for k, v in data.items()}

    def _save_metadata(self):
        """Save file metadata"""
        with open(self.metadata_path, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.files.items()}, f)

    def upload(self, filename: str, content: bytes, tags: List[str] = None) -> str:
        """Upload file"""
        file_hash = hashlib.sha256(content).hexdigest()
        file_id = file_hash[:16]

        # Save file
        file_path = os.path.join(self.storage_path, file_id)
        with open(file_path, 'wb') as f:
            f.write(content)

        # Save metadata
        import time
        meta = FileMetadata(
            id=file_id,
            filename=filename,
            size=len(content),
            hash=file_hash,
            created=time.time(),
            tags=tags or []
        )
        self.files[file_id] = meta
        self._save_metadata()

        return file_id

    def download(self, file_id: str) -> Optional[bytes]:
        """Download file"""
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        return None

    def delete(self, file_id: str):
        """Delete file"""
        file_path = os.path.join(self.storage_path, file_id)
        if os.path.exists(file_path):
            os.remove(file_path)
        if file_id in self.files:
            del self.files[file_id]
            self._save_metadata()

    def list_files(self, tags: List[str] = None) -> List[FileMetadata]:
        """List files"""
        files = list(self.files.values())
        if tags:
            files = [f for f in files if any(t in f.tags for t in tags)]
        return files

if __name__ == "__main__":
    storage = FileStorage("./test_storage")
    file_id = storage.upload("test.txt", b"Hello World", tags=["test"])
    content = storage.download(file_id)
    print(f"Downloaded: {content}")
    print(f"Files: {len(storage.list_files())}")
