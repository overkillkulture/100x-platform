"""
MODULE #35: VECTOR DATABASE
Built: 2025-11-08
Store and search high-dimensional vectors (embeddings).
"""

import numpy as np
from typing import List, Tuple, Dict, Any


class VectorDatabase:
    """Simple vector database with cosine similarity search"""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors = []
        self.metadata = []
        self.index = {}

    def insert(self, vector: np.ndarray, meta: Dict[str, Any]):
        """Insert vector with metadata"""
        if len(vector) != self.dimension:
            raise ValueError(f"Vector must be {self.dimension} dimensional")

        # Normalize
        norm_vector = vector / (np.linalg.norm(vector) + 1e-10)

        idx = len(self.vectors)
        self.vectors.append(norm_vector)
        self.metadata.append(meta)
        self.index[meta.get('id', idx)] = idx

    def search(self, query: np.ndarray, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar vectors"""
        if len(query) != self.dimension:
            raise ValueError(f"Query must be {self.dimension} dimensional")

        # Normalize query
        norm_query = query / (np.linalg.norm(query) + 1e-10)

        # Compute similarities
        similarities = []
        for i, vec in enumerate(self.vectors):
            sim = np.dot(norm_query, vec)
            similarities.append((self.metadata[i], float(sim)))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def delete(self, id: str):
        """Delete vector by ID"""
        if id in self.index:
            idx = self.index[id]
            del self.vectors[idx]
            del self.metadata[idx]
            del self.index[id]

    def stats(self):
        """Get database stats"""
        return {
            'dimension': self.dimension,
            'count': len(self.vectors),
            'size_bytes': len(self.vectors) * self.dimension * 8
        }


# Demo
if __name__ == "__main__":
    db = VectorDatabase(dimension=128)

    # Insert vectors
    for i in range(5):
        vec = np.random.randn(128)
        db.insert(vec, {'id': f'vec_{i}', 'type': 'embedding'})

    # Search
    query = np.random.randn(128)
    results = db.search(query, top_k=3)

    print(f"Search results:")
    for meta, score in results:
        print(f"  {meta['id']}: {score:.4f}")

    print(f"\nStats: {db.stats()}")
