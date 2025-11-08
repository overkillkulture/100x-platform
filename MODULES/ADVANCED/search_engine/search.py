"""MODULE #40: SEARCH ENGINE - Full-text search with ranking"""
import re
from typing import List, Dict, Set
from collections import defaultdict
import math

class SearchEngine:
    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.index: Dict[str, Set[str]] = defaultdict(set)  # term -> doc_ids
        self.doc_frequencies: Dict[str, int] = defaultdict(int)

    def add_document(self, doc_id: str, text: str):
        """Add document to index"""
        self.documents[doc_id] = text
        terms = self._tokenize(text)

        for term in set(terms):
            self.index[term].add(doc_id)
            self.doc_frequencies[term] += 1

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.split()

    def search(self, query: str, top_k: int = 10) -> List[tuple]:
        """Search documents"""
        query_terms = self._tokenize(query)

        # Find candidate documents
        candidates = set()
        for term in query_terms:
            candidates.update(self.index.get(term, set()))

        # Rank candidates using TF-IDF
        scores = []
        for doc_id in candidates:
            score = self._score_document(doc_id, query_terms)
            scores.append((doc_id, score))

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def _score_document(self, doc_id: str, query_terms: List[str]) -> float:
        """Calculate TF-IDF score"""
        doc_text = self.documents[doc_id]
        doc_terms = self._tokenize(doc_text)

        score = 0.0
        total_docs = len(self.documents)

        for term in query_terms:
            # Term frequency
            tf = doc_terms.count(term) / len(doc_terms) if doc_terms else 0

            # Inverse document frequency
            df = self.doc_frequencies.get(term, 0)
            idf = math.log((total_docs + 1) / (df + 1)) if df > 0 else 0

            score += tf * idf

        return score

if __name__ == "__main__":
    search = SearchEngine()

    # Add documents
    search.add_document("doc1", "Machine learning is transforming AI")
    search.add_document("doc2", "Deep learning models are powerful")
    search.add_document("doc3", "Natural language processing is amazing")

    # Search
    results = search.search("learning AI", top_k=2)
    print("Search results:")
    for doc_id, score in results:
        print(f"  {doc_id}: {score:.3f} - {search.documents[doc_id]}")
