# MODULE #39: FILE STORAGE
Cloud-style file storage with metadata, tags, and hash-based deduplication.
```python
from storage import FileStorage
storage = FileStorage("./files")
file_id = storage.upload("doc.pdf", content, tags=["important"])
content = storage.download(file_id)
```
**#39 COMPLETE** ✅
